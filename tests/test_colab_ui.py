import unittest

from src.whisper_colab import launch_colab_ui
from src.whisper_colab.colab_runner import (
    DEFAULT_OUTPUT_DIR,
    INPUT_MODE_DRIVE_FILE_PATHS,
    ColabTranscriptionConfig,
)
from src.whisper_colab.colab_ui import config_from_ui_values, ui_values_from_config


class ColabUiTests(unittest.TestCase):
    def test_launch_colab_ui_is_exported(self):
        self.assertTrue(callable(launch_colab_ui))

    def test_ui_values_from_config_joins_file_paths_for_textarea(self):
        config = ColabTranscriptionConfig(
            meeting_file_paths=[
                "/content/drive/MyDrive/one.mp4",
                "/content/drive/MyDrive/two.mp4",
            ]
        )

        values = ui_values_from_config(config)

        self.assertEqual(
            values["meeting_file_paths"],
            "/content/drive/MyDrive/one.mp4\n/content/drive/MyDrive/two.mp4",
        )

    def test_config_from_ui_values_parses_textarea_file_paths(self):
        config = config_from_ui_values(
            {
                "input_mode": INPUT_MODE_DRIVE_FILE_PATHS,
                "meeting_file_paths": "\n/content/drive/MyDrive/one.mp4\n\n/content/two.mp3\n",
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
                "export_zip": True,
                "download_individual_files": False,
                "zip_file_name": "outputs.zip",
                "max_segment_seconds": 1800,
                "install_packages": True,
            }
        )

        self.assertEqual(
            config.meeting_file_paths,
            ["/content/drive/MyDrive/one.mp4", "/content/two.mp3"],
        )
        self.assertEqual(config.custom_language, "Welsh")
        self.assertEqual(config.max_segment_seconds, 1800)


if __name__ == "__main__":
    unittest.main()
