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
    _build_output_locations_html,
    collect_gradio_input_paths,
    config_from_gradio_values,
    drive_input_interactivity,
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

    def test_drive_input_interactivity_follows_mount_setting(self):
        self.assertEqual(drive_input_interactivity(True), (True, True, True, True))
        self.assertEqual(drive_input_interactivity(False), (False, False, False, False))

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
            )

        self.assertIn("Processed 1 file", status)
        self.assertIn("/content/drive/MyDrive", locations)
        self.assertEqual(files, ["/content/whisper_outputs/outputs.zip"])
        self.assertFalse(run.call_args.kwargs["download_outputs"])


if __name__ == "__main__":
    unittest.main()
