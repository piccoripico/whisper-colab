import unittest
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch

from src.whisper_colab.colab_runner import (
    COLAB_REQUIREMENTS,
    COLAB_REQUIREMENTS_PATH,
    DEFAULT_DOWNLOAD_DIR,
    DEFAULT_OUTPUT_DIR,
    INPUT_MODE_DRIVE_FILE_PATHS,
    INPUT_MODE_DRIVE_FOLDER_PATH,
    INPUT_MODE_UPLOAD,
    LANGUAGE_AUTO,
    LANGUAGE_CUSTOM,
    LANGUAGE_OPTIONS,
    MODEL_OPTIONS,
    ColabTranscriptionConfig,
    _build_generate_kwargs,
    _build_transcript,
    _collect_drive_folder_paths,
    _create_zip_archive,
    _download_outputs,
    _download_zip_path,
    _merge_transcriptions,
    _normalize_input_mode,
    _normalize_language,
    _normalize_max_segment_seconds,
    _output_dir_for_source,
    _prepare_downloadable_outputs,
    _resolve_torch_device,
    _run_transcription_pipeline,
    _save_outputs,
    _split_audio_for_transcription,
    _transcribe_audio_segments,
    _validate_config,
    _validate_media_files,
)


class ColabRunnerTests(unittest.TestCase):
    def test_model_and_language_options_expose_expected_defaults(self):
        self.assertEqual(MODEL_OPTIONS[0], "openai/whisper-large-v3-turbo")
        self.assertIn("openai/whisper-large-v3", MODEL_OPTIONS)
        self.assertEqual(LANGUAGE_OPTIONS[0], LANGUAGE_AUTO)
        self.assertIn(LANGUAGE_CUSTOM, LANGUAGE_OPTIONS)
        self.assertIn("japanese", LANGUAGE_OPTIONS)
        self.assertIn("english", LANGUAGE_OPTIONS)
        self.assertIn("welsh", LANGUAGE_OPTIONS)
        self.assertEqual(ColabTranscriptionConfig().output_dir, DEFAULT_OUTPUT_DIR)
        self.assertTrue(ColabTranscriptionConfig().download_zip_on_completion)

    def test_colab_requirements_file_exists_for_runtime_install(self):
        self.assertTrue(COLAB_REQUIREMENTS_PATH.exists())
        text = COLAB_REQUIREMENTS_PATH.read_text(encoding="utf-8")
        for requirement in COLAB_REQUIREMENTS:
            self.assertIn(requirement, text)

    def test_build_generate_kwargs_defaults_to_auto_language_transcription(self):
        config = ColabTranscriptionConfig()

        self.assertEqual(_build_generate_kwargs(config), {"task": "transcribe"})

    def test_build_generate_kwargs_with_source_language(self):
        config = ColabTranscriptionConfig(language="japanese")

        self.assertEqual(
            _build_generate_kwargs(config),
            {"task": "transcribe", "language": "japanese"},
        )

    def test_build_generate_kwargs_for_translation_to_english(self):
        config = ColabTranscriptionConfig(
            language="japanese",
            translate_to_english=True,
        )

        self.assertEqual(
            _build_generate_kwargs(config),
            {"task": "translate", "language": "japanese"},
        )

    def test_build_generate_kwargs_preserves_legacy_japanese_flag(self):
        config = ColabTranscriptionConfig(is_japanese_language=True)

        self.assertEqual(
            _build_generate_kwargs(config),
            {"task": "transcribe", "language": "japanese"},
        )

    def test_normalize_language_treats_auto_as_unspecified(self):
        self.assertIsNone(_normalize_language("auto"))
        self.assertIsNone(_normalize_language(""))
        self.assertEqual(_normalize_language(" English "), "english")

    def test_build_generate_kwargs_uses_custom_language(self):
        config = ColabTranscriptionConfig(
            language=LANGUAGE_CUSTOM,
            custom_language="Welsh",
        )

        self.assertEqual(
            _build_generate_kwargs(config),
            {"task": "transcribe", "language": "welsh"},
        )

    def test_validate_config_rejects_missing_custom_language(self):
        config = ColabTranscriptionConfig(language=LANGUAGE_CUSTOM)

        with self.assertRaisesRegex(ValueError, "custom_language"):
            _validate_config(config)

    def test_validate_config_rejects_empty_model(self):
        config = ColabTranscriptionConfig(model_id=" ")

        with self.assertRaisesRegex(ValueError, "model_id"):
            _validate_config(config)

    def test_resolve_torch_device_uses_cuda_when_available(self):
        torch = _FakeTorch(cuda_available=True)

        self.assertEqual(
            _resolve_torch_device(torch, require_gpu=True),
            ("cuda:0", "float16"),
        )

    def test_resolve_torch_device_rejects_cpu_when_gpu_is_required(self):
        torch = _FakeTorch(cuda_available=False)

        with self.assertRaisesRegex(RuntimeError, "CUDA GPU is required"):
            _resolve_torch_device(torch, require_gpu=True)

    def test_resolve_torch_device_can_fallback_to_cpu(self):
        torch = _FakeTorch(cuda_available=False)

        self.assertEqual(
            _resolve_torch_device(torch, require_gpu=False),
            ("cpu", "float32"),
        )

    def test_normalize_max_segment_seconds(self):
        self.assertEqual(_normalize_max_segment_seconds("1800"), 1800)
        with self.assertRaisesRegex(ValueError, "max_segment_seconds"):
            _normalize_max_segment_seconds("-1")

    def test_build_transcript_with_timestamps(self):
        transcription = {
            "chunks": [
                {"timestamp": (0.0, 2.0), "text": " Hello "},
                {"timestamp": (65.2, 68.0), "text": "world"},
            ]
        }

        self.assertEqual(
            _build_transcript(transcription, include_timestamps=True),
            "[00:00:00] Hello\n[00:01:05] world\n",
        )

    def test_build_transcript_without_chunks(self):
        self.assertEqual(
            _build_transcript({"text": "plain text"}, include_timestamps=True),
            "plain text\n",
        )

    def test_normalize_input_mode_keeps_explicit_mode(self):
        config = ColabTranscriptionConfig(input_mode=INPUT_MODE_DRIVE_FOLDER_PATH)

        self.assertEqual(_normalize_input_mode(config), INPUT_MODE_DRIVE_FOLDER_PATH)

    def test_normalize_input_mode_preserves_legacy_google_drive_flag(self):
        config = ColabTranscriptionConfig(
            input_mode=INPUT_MODE_UPLOAD,
            use_google_drive_files=True,
        )

        self.assertEqual(_normalize_input_mode(config), INPUT_MODE_DRIVE_FILE_PATHS)

    def test_collect_drive_folder_paths_finds_supported_media(self):
        with TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)
            (folder / "meeting.mp4").write_bytes(b"video")
            (folder / "audio.MP3").write_bytes(b"audio")
            (folder / "notes.txt").write_text("skip", encoding="utf-8")

            paths = _collect_drive_folder_paths(str(folder), recursive=False)

        self.assertEqual([path.name for path in paths], ["audio.MP3", "meeting.mp4"])

    def test_collect_drive_folder_paths_can_recurse(self):
        with TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)
            nested = folder / "nested"
            nested.mkdir()
            (nested / "meeting.m4a").write_bytes(b"audio")

            paths = _collect_drive_folder_paths(str(folder), recursive=True)

        self.assertEqual([path.name for path in paths], ["meeting.m4a"])

    def test_validate_media_files_rejects_unsupported_extension(self):
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "notes.txt"
            path.write_text("not media", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Unsupported media extension"):
                _validate_media_files([path])

    def test_save_outputs_uses_output_dir_and_unique_names(self):
        with TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            used_paths = set()
            source_path = Path("/content/input/meeting.mp4")

            first = _save_outputs(
                source_path=source_path,
                transcription={"text": "first"},
                include_timestamps=True,
                export_excel=False,
                output_dir=output_dir,
                used_output_paths=used_paths,
            )
            second = _save_outputs(
                source_path=source_path,
                transcription={"text": "second"},
                include_timestamps=True,
                export_excel=False,
                output_dir=output_dir,
                used_output_paths=used_paths,
            )

            self.assertEqual(first, [output_dir / "meeting.mp4.txt"])
            self.assertEqual(second, [output_dir / "meeting.mp4_2.txt"])
            self.assertEqual(
                (output_dir / "meeting.mp4.txt").read_text(encoding="utf-8"), "first\n"
            )

    def test_create_zip_archive_contains_saved_outputs(self):
        with TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            first = output_dir / "one.txt"
            second = output_dir / "two.txt"
            first.write_text("one", encoding="utf-8")
            second.write_text("two", encoding="utf-8")

            zip_path = _create_zip_archive([first, second], output_dir / "outputs.zip")

            with zipfile.ZipFile(zip_path) as archive:
                self.assertEqual(sorted(archive.namelist()), ["one.txt", "two.txt"])

    def test_download_outputs_can_download_only_zip(self):
        with TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            first = output_dir / "one.txt"
            first.write_text("one", encoding="utf-8")
            files_module = _FakeFilesModule()

            _download_outputs(
                output_paths=[first],
                config=ColabTranscriptionConfig(
                    output_dir=str(output_dir),
                    export_zip=True,
                    download_individual_files=False,
                    zip_file_name="bundle.zip",
                ),
                output_dir=output_dir,
                files_module=files_module,
            )

            self.assertEqual(files_module.downloaded_paths, [str(output_dir / "bundle.zip")])

    def test_prepare_downloadable_outputs_can_return_temporary_zip(self):
        with TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            first = output_dir / "one.txt"
            first.write_text("one", encoding="utf-8")

            paths = _prepare_downloadable_outputs(
                output_paths=[first],
                config=ColabTranscriptionConfig(
                    output_dir=str(output_dir),
                    download_zip_on_completion=True,
                    zip_file_name="bundle.zip",
                ),
                output_dir=output_dir,
            )

            self.assertEqual(paths, [output_dir.parent / "whisper_downloads" / "bundle.zip"])
            self.assertTrue((output_dir.parent / "whisper_downloads" / "bundle.zip").exists())

    def test_prepare_downloadable_outputs_can_return_no_download(self):
        with TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            first = output_dir / "one.txt"
            first.write_text("one", encoding="utf-8")

            paths = _prepare_downloadable_outputs(
                output_paths=[first],
                config=ColabTranscriptionConfig(download_zip_on_completion=False),
                output_dir=output_dir,
            )

            self.assertEqual(paths, [])

    def test_output_dir_defaults_to_source_folder(self):
        source_path = Path("/content/drive/MyDrive/input/meeting.mp4")

        output_dir = _output_dir_for_source(ColabTranscriptionConfig(), source_path)

        self.assertEqual(output_dir, source_path.parent)

    def test_output_dir_uses_default_for_upload(self):
        source_path = Path("/content/meeting.mp4")

        output_dir = _output_dir_for_source(
            ColabTranscriptionConfig(input_mode=INPUT_MODE_UPLOAD),
            source_path,
        )

        self.assertEqual(output_dir, Path(DEFAULT_OUTPUT_DIR))

    def test_output_dir_can_use_custom_folder(self):
        with TemporaryDirectory() as temp_dir:
            custom_dir = Path(temp_dir) / "custom"

            output_dir = _output_dir_for_source(
                ColabTranscriptionConfig(
                    use_custom_output_dir=True,
                    output_dir=str(custom_dir),
                ),
                Path("/content/drive/MyDrive/input/meeting.mp4"),
            )

        self.assertEqual(output_dir, custom_dir)

    def test_colab_download_zip_path_uses_download_dir(self):
        path = _download_zip_path(
            ColabTranscriptionConfig(zip_file_name="bundle.zip"),
            Path("/content/whisper_outputs"),
        )

        self.assertEqual(path, Path(DEFAULT_DOWNLOAD_DIR) / "bundle.zip")

    def test_pipeline_without_download_returns_downloadable_files(self):
        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            input_path = temp_path / "meeting.mp4"
            input_path.write_bytes(b"video")

            with (
                patch(
                    "src.whisper_colab.colab_runner.extract_audio_for_whisper",
                    return_value=temp_path / "meeting.wav",
                ),
                patch(
                    "src.whisper_colab.colab_runner._split_audio_for_transcription",
                    return_value=[temp_path / "meeting.wav"],
                ),
                patch("src.whisper_colab.colab_runner._load_whisper_pipeline") as load_pipe,
            ):
                load_pipe.return_value = lambda *_args, **_kwargs: {"text": "done"}
                results = _run_transcription_pipeline(
                    config=ColabTranscriptionConfig(
                        output_dir=str(temp_path / "out"),
                        export_excel=False,
                        use_custom_output_dir=True,
                        download_zip_on_completion=True,
                    ),
                    input_paths=[input_path],
                    download_outputs=False,
                )

            self.assertEqual(
                results[0]["downloadable_files"],
                [str(temp_path / "whisper_downloads" / "whisper_outputs.zip")],
            )
            self.assertEqual(results[0]["output_dir"], str(temp_path / "out"))
            self.assertFalse((temp_path / "out" / "whisper_outputs.zip").exists())

    def test_split_audio_for_transcription_builds_segment_command(self):
        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            audio_path = temp_path / "meeting.whisper.wav"
            audio_path.write_bytes(b"audio")

            def fake_run(command, **_kwargs):
                segment_path = Path(command[-1].replace("%03d", "000"))
                segment_path.parent.mkdir(parents=True, exist_ok=True)
                segment_path.write_bytes(b"segment")
                return _CompletedProcess(command)

            with patch(
                "src.whisper_colab.colab_runner.subprocess.run", side_effect=fake_run
            ) as run:
                segments = _split_audio_for_transcription(
                    audio_path,
                    output_dir=temp_path / "audio",
                    max_segment_seconds=60,
                )

            self.assertEqual(len(segments), 1)
            self.assertIn("-segment_time", run.call_args.args[0])
            self.assertIn("60", run.call_args.args[0])

    def test_transcribe_audio_segments_offsets_and_merges_timestamps(self):
        segment_paths = [Path("part000.wav"), Path("part001.wav")]

        def fake_pipe(path, **_kwargs):
            name = Path(path).name
            return {
                "text": name,
                "chunks": [
                    {
                        "timestamp": (1.0, 2.0),
                        "text": name,
                    }
                ],
            }

        transcription = _transcribe_audio_segments(
            pipe=fake_pipe,
            segment_paths=segment_paths,
            generate_kwargs={"task": "transcribe"},
            progress_prefix="[1/1]",
            max_segment_seconds=30,
        )

        self.assertEqual(transcription["text"], "part000.wav part001.wav")
        self.assertEqual(transcription["chunks"][1]["timestamp"], (31.0, 32.0))

    def test_merge_transcriptions_keeps_single_transcription_unchanged(self):
        transcription = {"text": "one"}

        self.assertIs(_merge_transcriptions([transcription]), transcription)


class _FakeFilesModule:
    def __init__(self):
        self.downloaded_paths = []

    def download(self, path):
        self.downloaded_paths.append(path)


class _CompletedProcess:
    def __init__(self, args):
        self.args = args
        self.returncode = 0
        self.stdout = ""
        self.stderr = ""


class _FakeTorch:
    float16 = "float16"
    float32 = "float32"

    def __init__(self, *, cuda_available):
        self.cuda = SimpleNamespace(is_available=lambda: cuda_available)


if __name__ == "__main__":
    unittest.main()
