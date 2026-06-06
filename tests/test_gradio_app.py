import inspect
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch

from src.whisper_colab import launch_gradio_app
from src.whisper_colab.colab_runner import (
    DEFAULT_OUTPUT_DIR,
    INPUT_MODE_DRIVE_FILE_PATHS,
    INPUT_MODE_DRIVE_FILE_PICKER,
    INPUT_MODE_DRIVE_FOLDER_PICKER,
    INPUT_MODE_UPLOAD,
)
from src.whisper_colab.gradio_app import (
    LANGUAGE_CHOICES,
    _build_auto_download_html,
    _build_gradio_blocks,
    _build_output_locations_html,
    _drive_picker_root,
    _is_drive_picker_available,
    _upload_details,
    collect_gradio_input_paths,
    config_from_gradio_values,
    drive_input_interactivity,
    initial_input_mode,
    input_mode_options,
    input_section_visibility,
    ui_values_from_config,
)


class GradioAppTests(unittest.TestCase):
    def test_launch_gradio_app_is_exported(self):
        self.assertTrue(callable(launch_gradio_app))

    def test_ui_values_from_config_joins_file_paths_for_textbox(self):
        from src.whisper_colab.colab_runner import ColabTranscriptionConfig

        config = ColabTranscriptionConfig(
            meeting_file_paths=[
                "/content/drive/MyDrive/one.mp4",
                "/content/drive/MyDrive/two.mp4",
            ]
        )

        values = ui_values_from_config(config)

        self.assertEqual(
            values["drive_file_paths"],
            "/content/drive/MyDrive/one.mp4\n/content/drive/MyDrive/two.mp4",
        )

    def test_config_from_gradio_values_parses_textbox_file_paths(self):
        config = config_from_gradio_values(
            {
                "input_mode": INPUT_MODE_DRIVE_FILE_PATHS,
                "drive_file_paths": "\n/content/drive/MyDrive/one.mp4\n\n/content/two.mp3\n",
                "drive_folder_path": "/content/drive/MyDrive/input",
                "drive_recursive": True,
                "model_id": "openai/whisper-large-v3-turbo",
                "language": "custom",
                "custom_language": "Welsh",
                "translate_to_english": False,
                "include_timestamps": True,
                "export_excel": True,
                "audio_output_dir": "/content/audio",
                "output_dir": DEFAULT_OUTPUT_DIR,
                "use_custom_output_dir": False,
                "download_zip_on_completion": True,
                "zip_file_name": "outputs.zip",
                "max_segment_seconds": 1800,
                "mount_google_drive": True,
                "pipeline_chunk_length_s": 0,
                "pipeline_batch_size": 0,
                "generate_num_beams": 0,
                "generate_temperature": "",
                "generate_condition_on_prev_tokens": "",
                "generate_compression_ratio_threshold": "",
                "generate_logprob_threshold": "",
                "generate_no_speech_threshold": "",
                "model_attn_implementation": "",
            }
        )

        self.assertEqual(
            config.meeting_file_paths,
            ["/content/drive/MyDrive/one.mp4", "/content/two.mp3"],
        )
        self.assertEqual(config.custom_language, "Welsh")
        self.assertEqual(config.max_segment_seconds, 1800)
        self.assertFalse(config.install_packages)
        self.assertTrue(config.require_gpu)
        self.assertTrue(config.mount_google_drive)
        self.assertFalse(config.use_custom_output_dir)
        self.assertTrue(config.download_zip_on_completion)

    def test_config_from_gradio_values_maps_optional_parameters(self):
        config = config_from_gradio_values(
            {
                "input_mode": INPUT_MODE_DRIVE_FILE_PATHS,
                "drive_file_paths": "",
                "drive_folder_path": "/content/drive/MyDrive/input",
                "drive_recursive": False,
                "model_id": "openai/whisper-large-v3-turbo",
                "language": "auto",
                "custom_language": "",
                "translate_to_english": False,
                "include_timestamps": True,
                "export_excel": True,
                "audio_output_dir": "/content/audio",
                "output_dir": DEFAULT_OUTPUT_DIR,
                "use_custom_output_dir": False,
                "download_zip_on_completion": True,
                "zip_file_name": "outputs.zip",
                "max_segment_seconds": 0,
                "mount_google_drive": True,
                "pipeline_chunk_length_s": 30,
                "pipeline_batch_size": 8,
                "generate_num_beams": 4,
                "generate_temperature": "0.1",
                "generate_condition_on_prev_tokens": "false",
                "generate_compression_ratio_threshold": "2.4",
                "generate_logprob_threshold": "-1.0",
                "generate_no_speech_threshold": "0.6",
                "model_attn_implementation": "sdpa",
            }
        )

        self.assertEqual(config.pipeline_chunk_length_s, 30)
        self.assertEqual(config.pipeline_batch_size, 8)
        self.assertEqual(config.generate_num_beams, 4)
        self.assertEqual(config.generate_temperature, "0.1")
        self.assertEqual(config.generate_condition_on_prev_tokens, "false")
        self.assertEqual(config.model_attn_implementation, "sdpa")

    def test_drive_input_interactivity_follows_mount_setting(self):
        self.assertEqual(drive_input_interactivity(True), (True, True, True, True))
        self.assertEqual(drive_input_interactivity(False), (False, False, False, False))

    def test_drive_picker_uses_existing_disabled_root_when_drive_is_unavailable(self):
        root = _drive_picker_root(False)

        self.assertTrue(root.exists())
        self.assertTrue(root.is_dir())

    def test_drive_picker_availability_requires_existing_drive_root(self):
        with TemporaryDirectory() as temp_dir:
            drive_root = Path(temp_dir) / "missing"

            self.assertFalse(_is_drive_picker_available(True, drive_root))
            self.assertFalse(_is_drive_picker_available(False, drive_root))

    def test_input_mode_options_hide_drive_modes_when_drive_is_unavailable(self):
        self.assertEqual(input_mode_options(False), [("Upload local files", INPUT_MODE_UPLOAD)])
        self.assertEqual(initial_input_mode(INPUT_MODE_DRIVE_FILE_PICKER, False), INPUT_MODE_UPLOAD)
        self.assertIn(
            ("Pick Drive files", INPUT_MODE_DRIVE_FILE_PICKER),
            input_mode_options(True),
        )
        self.assertIn(
            ("Pick Drive folders", INPUT_MODE_DRIVE_FOLDER_PICKER),
            input_mode_options(True),
        )

    def test_language_choices_use_title_case_labels_and_lowercase_values(self):
        self.assertIn(("Auto", "auto"), LANGUAGE_CHOICES)
        self.assertIn(("Custom", "custom"), LANGUAGE_CHOICES)
        self.assertIn(("Japanese", "japanese"), LANGUAGE_CHOICES)

    def test_gradio_source_filters_picker_visibility_and_hides_zip_initially(self):
        source = inspect.getsource(_build_gradio_blocks)

        self.assertIn('glob="**/"', source)
        self.assertIn('ignore_glob="**/*.*"', source)
        self.assertIn('ignore_glob="**/"', source)
        self.assertIn('visible=values["use_custom_output_dir"]', source)
        self.assertIn('visible=values["download_zip_on_completion"]', source)
        self.assertIn('visible=values["language"] == "custom"', source)
        self.assertIn('label="Source language"', source)
        self.assertIn('label="Split seconds"', source)
        self.assertIn("visible=False", source)
        self.assertIn('label="Require GPU"', source)
        self.assertIn('title="Whisper Colab App"', source)
        self.assertIn("visible=False", source)
        self.assertIn("outputs are also saved in folders", source)
        self.assertNotIn(
            'gr.FileExplorer(\n                    root_dir=str(drive_picker_root),\n                    glob="**/",\n                    ignore_glob="**/*.*",\n                    file_count="multiple",\n                    label="Drive folder picker",\n                    info=',
            source,
        )
        self.assertNotIn(
            'gr.FileExplorer(\n                    root_dir=str(drive_picker_root),\n                    glob=media_glob,\n                    ignore_glob="**/",\n                    file_count="multiple",\n                    label="Drive file picker",\n                    info=',
            source,
        )

    def test_input_section_visibility_matches_selected_input_mode(self):
        self.assertEqual(
            input_section_visibility(INPUT_MODE_DRIVE_FILE_PICKER),
            (False, True, False, False, False),
        )
        self.assertEqual(
            input_section_visibility(INPUT_MODE_UPLOAD),
            (False, False, False, False, True),
        )

    def test_drive_file_picker_collects_selected_files(self):
        with TemporaryDirectory() as temp_dir:
            drive_root = Path(temp_dir)
            file_path = drive_root / "meeting.mp4"
            file_path.write_bytes(b"video")

            paths = collect_gradio_input_paths(
                input_mode=INPUT_MODE_DRIVE_FILE_PICKER,
                drive_file_picker=[{"path": "meeting.mp4"}],
                drive_folder_picker=None,
                drive_file_paths="",
                drive_folder_path="",
                uploaded_files=None,
                drive_recursive=False,
                drive_root=drive_root,
            )

        self.assertEqual(paths, [file_path])

    def test_drive_file_picker_collects_file_like_selected_files(self):
        with TemporaryDirectory() as temp_dir:
            drive_root = Path(temp_dir)
            file_path = drive_root / "meeting.mp4"
            file_path.write_bytes(b"video")

            paths = collect_gradio_input_paths(
                input_mode=INPUT_MODE_DRIVE_FILE_PICKER,
                drive_file_picker=[SimpleNamespace(name="meeting.mp4")],
                drive_folder_picker=None,
                drive_file_paths="",
                drive_folder_path="",
                uploaded_files=None,
                drive_recursive=False,
                drive_root=drive_root,
            )

        self.assertEqual(paths, [file_path])

    def test_drive_file_picker_accepts_file_url_like_selection(self):
        with TemporaryDirectory() as temp_dir:
            drive_root = Path(temp_dir)
            file_path = drive_root / "meeting.mp4"
            file_path.write_bytes(b"video")

            paths = collect_gradio_input_paths(
                input_mode=INPUT_MODE_DRIVE_FILE_PICKER,
                drive_file_picker=[f"file={file_path.as_posix()}"],
                drive_folder_picker=None,
                drive_file_paths="",
                drive_folder_path="",
                uploaded_files=None,
                drive_recursive=False,
                drive_root=drive_root,
            )

        self.assertEqual(paths, [file_path])

    def test_drive_file_picker_accepts_root_relative_absolute_selection(self):
        with TemporaryDirectory() as temp_dir:
            drive_root = Path(temp_dir)
            file_path = drive_root / "meeting.mp4"
            file_path.write_bytes(b"video")

            paths = collect_gradio_input_paths(
                input_mode=INPUT_MODE_DRIVE_FILE_PICKER,
                drive_file_picker=["/meeting.mp4"],
                drive_folder_picker=None,
                drive_file_paths="",
                drive_folder_path="",
                uploaded_files=None,
                drive_recursive=False,
                drive_root=drive_root,
            )

        self.assertEqual(paths, [file_path])

    def test_drive_folder_picker_expands_supported_media(self):
        with TemporaryDirectory() as temp_dir:
            drive_root = Path(temp_dir)
            folder = drive_root / "recordings"
            folder.mkdir()
            (folder / "meeting.mp4").write_bytes(b"video")
            (folder / "notes.txt").write_text("skip", encoding="utf-8")

            paths = collect_gradio_input_paths(
                input_mode=INPUT_MODE_DRIVE_FOLDER_PICKER,
                drive_file_picker=None,
                drive_folder_picker="recordings",
                drive_file_paths="",
                drive_folder_path="",
                uploaded_files=None,
                drive_recursive=False,
                drive_root=drive_root,
            )

        self.assertEqual(paths, [folder / "meeting.mp4"])

    def test_drive_folder_picker_expands_multiple_supported_folders(self):
        with TemporaryDirectory() as temp_dir:
            drive_root = Path(temp_dir)
            folder_one = drive_root / "one"
            folder_two = drive_root / "two"
            folder_one.mkdir()
            folder_two.mkdir()
            (folder_one / "one.mp4").write_bytes(b"video")
            (folder_two / "two.mp3").write_bytes(b"audio")

            paths = collect_gradio_input_paths(
                input_mode=INPUT_MODE_DRIVE_FOLDER_PICKER,
                drive_file_picker=None,
                drive_folder_picker=["one", "two"],
                drive_file_paths="",
                drive_folder_path="",
                uploaded_files=None,
                drive_recursive=False,
                drive_root=drive_root,
            )

        self.assertEqual(paths, [folder_one / "one.mp4", folder_two / "two.mp3"])

    def test_drive_file_picker_rejects_selected_folder(self):
        with TemporaryDirectory() as temp_dir:
            drive_root = Path(temp_dir)
            (drive_root / "folder").mkdir()

            with self.assertRaisesRegex(IsADirectoryError, "selection is a folder"):
                collect_gradio_input_paths(
                    input_mode=INPUT_MODE_DRIVE_FILE_PICKER,
                    drive_file_picker=["folder"],
                    drive_folder_picker=None,
                    drive_file_paths="",
                    drive_folder_path="",
                    uploaded_files=None,
                    drive_recursive=False,
                    drive_root=drive_root,
                )

    def test_drive_folder_picker_rejects_selected_file(self):
        with TemporaryDirectory() as temp_dir:
            drive_root = Path(temp_dir)
            (drive_root / "meeting.mp4").write_bytes(b"video")

            with self.assertRaisesRegex(NotADirectoryError, "not a folder"):
                collect_gradio_input_paths(
                    input_mode=INPUT_MODE_DRIVE_FOLDER_PICKER,
                    drive_file_picker=None,
                    drive_folder_picker="meeting.mp4",
                    drive_file_paths="",
                    drive_folder_path="",
                    uploaded_files=None,
                    drive_recursive=False,
                    drive_root=drive_root,
                )

    def test_drive_input_requires_mount_enabled(self):
        with self.assertRaisesRegex(ValueError, "Mount Google Drive"):
            collect_gradio_input_paths(
                input_mode=INPUT_MODE_DRIVE_FILE_PICKER,
                drive_file_picker=["meeting.mp4"],
                drive_folder_picker=None,
                drive_file_paths="",
                drive_folder_path="",
                uploaded_files=None,
                drive_recursive=False,
                mount_google_drive=False,
            )

    def test_drive_picker_rejects_paths_outside_drive_root(self):
        with TemporaryDirectory() as temp_dir:
            drive_root = Path(temp_dir) / "drive"
            outside = Path(temp_dir) / "outside.mp4"
            drive_root.mkdir()
            outside.write_bytes(b"video")

            with self.assertRaisesRegex(ValueError, "outside the allowed Drive root"):
                collect_gradio_input_paths(
                    input_mode=INPUT_MODE_DRIVE_FILE_PICKER,
                    drive_file_picker=[outside],
                    drive_folder_picker=None,
                    drive_file_paths="",
                    drive_folder_path="",
                    uploaded_files=None,
                    drive_recursive=False,
                    drive_root=drive_root,
                )

    def test_upload_collects_uploaded_file_paths(self):
        with TemporaryDirectory() as temp_dir:
            upload = Path(temp_dir) / "meeting.mp3"
            upload.write_bytes(b"audio")

            paths = collect_gradio_input_paths(
                input_mode=INPUT_MODE_UPLOAD,
                drive_file_picker=None,
                drive_folder_picker=None,
                drive_file_paths="",
                drive_folder_path="",
                uploaded_files=[SimpleNamespace(name=str(upload))],
                drive_recursive=False,
            )

        self.assertEqual(paths, [upload])

    def test_upload_details_shows_file_size_and_completion(self):
        with TemporaryDirectory() as temp_dir:
            upload = Path(temp_dir) / "meeting.mp3"
            upload.write_bytes(b"audio")

            details = _upload_details([SimpleNamespace(name=str(upload))])

        self.assertIn("Upload complete: 100%", details)
        self.assertIn("meeting.mp3", details)

    def test_output_locations_html_lists_output_folders(self):
        html = _build_output_locations_html(
            [
                {"output_dir": "/content/drive/MyDrive/one"},
                {"output_dir": "/content/drive/MyDrive/two"},
                {"output_dir": "/content/drive/MyDrive/one"},
            ]
        )

        self.assertIn("/content/drive/MyDrive/one", html)
        self.assertIn("/content/drive/MyDrive/two", html)
        self.assertIn("<a href=", html)

    def test_auto_download_html_includes_script_and_manual_link(self):
        html = _build_auto_download_html(["/content/whisper_downloads/outputs.zip"])

        self.assertIn("download the ZIP file manually", html)
        self.assertIn("link.click()", html)
        self.assertIn("/file=", html)

    def test_gradio_run_returns_status_locations_and_zip_without_colab_download(self):
        from src.whisper_colab import gradio_app

        result = {
            "source_path": "/content/drive/MyDrive/meeting.mp4",
            "output_dir": "/content/drive/MyDrive",
            "downloadable_files": ["/content/whisper_outputs/outputs.zip"],
        }

        with (
            patch.object(
                gradio_app, "collect_gradio_input_paths", return_value=[Path("meeting.mp4")]
            ),
            patch.object(gradio_app, "run_transcription_for_paths", return_value=[result]) as run,
        ):
            status, locations, files = gradio_app._run_from_gradio(
                INPUT_MODE_DRIVE_FILE_PICKER,
                None,
                ["meeting.mp4"],
                "",
                "",
                None,
                False,
                "openai/whisper-large-v3-turbo",
                "auto",
                "",
                False,
                0,
                True,
                True,
                True,
                False,
                DEFAULT_OUTPUT_DIR,
                True,
                "outputs.zip",
                "/content/whisper_audio",
                True,
                0,
                0,
                0,
                "",
                "",
                "",
                "",
                "",
                "",
            )

        self.assertIn("Processed 1 file", status)
        self.assertIn("/content/drive/MyDrive", locations)
        self.assertEqual(files, ["/content/whisper_outputs/outputs.zip"])
        self.assertFalse(run.call_args.kwargs["download_outputs"])


if __name__ == "__main__":
    unittest.main()
