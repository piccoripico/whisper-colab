# whisper-colab

A thin Google Colab notebook for transcribing audio and video files with Whisper.

[Open in Colab](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/Whisper_v3.ipynb)

## What this repository does

- Keeps the notebook small: user settings stay in the notebook, while the workflow lives in `src/whisper_colab`.
- Converts input audio or video to Whisper-friendly WAV before transcription.
- Uses `16 kHz / mono / PCM WAV` extraction through `ffmpeg`.
- Lets you choose `openai/whisper-large-v3-turbo` or `openai/whisper-large-v3`.
- Lets Whisper auto-detect the language by default, lets you select a source language, or lets you enter a custom language name.
- Downloads transcript outputs as `.txt` and, optionally, `.xlsx`.
- Saves outputs to a dedicated output directory and can download them as a ZIP archive.
- Can optionally split long extracted audio into fixed-length segments before transcription.

## Colab usage

1. Open `Whisper_v3.ipynb` in Google Colab.
2. Edit the settings cell.
3. Run the bootstrap/run cell.
4. Choose an input mode:
   - `upload`: upload local files to the Colab runtime.
   - `drive_file_paths`: enter one or more Google Drive file paths manually.
   - `drive_folder_path`: enter a Google Drive folder path and process supported media files in that folder.
   - `drive_file_picker`: pick one file from mounted Google Drive with a small notebook widget.
   - `drive_folder_picker`: pick one folder from mounted Google Drive with a small notebook widget.
5. Leave `LANGUAGE` as `auto` unless you want to force a source language.
6. Select `custom` and set `CUSTOM_LANGUAGE` only when the language you need is not in the list.
7. Enable `TRANSLATE_TO_ENGLISH` only when you want Whisper's translation task. Whisper translates speech to English, not to an arbitrary target language.
8. Keep `MAX_SEGMENT_SECONDS` at `0` for normal runs. Set it to a positive value, such as `1800`, only when a long recording needs to be split before transcription.
9. Use `OUTPUT_DIR`, `EXPORT_ZIP`, and `DOWNLOAD_INDIVIDUAL_FILES` to control where transcript files are saved and how they are downloaded.

The notebook clones this repository from:

```text
https://github.com/piccoripico/whisper-colab.git
```

## Generated notebook

`Whisper_v3.ipynb` is generated from `scripts/build_notebook.py`. Edit the script, then rebuild the notebook:

```powershell
python scripts/build_notebook.py
```

## Colab dependencies

Colab runtime dependencies are listed in `requirements-colab.txt`.

When `INSTALL_PACKAGES` is enabled, the runner:

1. Installs `ffmpeg` through `apt-get` only if it is missing.
2. Upgrades `pip`.
3. Installs packages from `requirements-colab.txt`.
4. Writes `/content/upgrades_done.flag` so the same runtime does not repeat the Python package installation.

Disable `INSTALL_PACKAGES` only when you have already prepared the runtime manually.

## Known limitations

- Whisper can hallucinate common phrases during silence, especially at the beginning of recordings. This repository does not remove those phrases in post-processing.
- Very long recordings may fail when the Colab runtime runs out of GPU or system memory.
- Segmenting long audio with `MAX_SEGMENT_SECONDS` can make long files easier to process, but timestamps are offset by segment length and may be approximate around segment boundaries.
- `ffmpeg` must be available. It is normally available in Colab, and the runner installs it when needed.

## Common failures

### No audio stream was found

The selected input file does not have a usable first audio stream. Try another source file, or manually check the file with `ffmpeg` or a media player.

### ffmpeg failed to extract audio

The input container or codec could not be decoded by the available `ffmpeg`. Re-encoding the file to a standard MP4 or MP3 before uploading often fixes this.

### Drive path does not exist

For Google Drive modes, mount Drive in Colab and check that paths begin with `/content/drive/MyDrive/`.

### Colab runs out of memory

Use `openai/whisper-large-v3-turbo`, reduce the number of files in one run, or set `MAX_SEGMENT_SECONDS` to split long extracted audio.

### Picker mode does not appear

Picker modes require `ipywidgets`. Keep `INSTALL_PACKAGES` enabled, rerun the notebook cell, and reload the Colab page if the widget still does not render.

## Local tests

```powershell
python scripts/build_notebook.py --check
ruff format --check .
ruff check .
python -m unittest
```

The same checks run in GitHub Actions on pushes to `main` and on pull requests.

## License

MIT License
