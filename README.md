# whisper-colab

A thin Google Colab notebook for transcribing audio and video files with Whisper.

[Open in Colab](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/Whisper_v3.ipynb)

## What this repository does

- Keeps the notebook small: it only clones the repository and launches the app.
- Launches a Gradio app in a separate browser tab from one Colab cell.
- Uses Google Drive picker modes as the main input path.
- Falls back to upload-only input when Google Drive is not mounted.
- Converts input audio or video to Whisper-friendly WAV before transcription.
- Uses `16 kHz / mono / PCM WAV` extraction through `ffmpeg`.
- Lets you choose `openai/whisper-large-v3-turbo` or `openai/whisper-large-v3`.
- Lets Whisper auto-detect the language by default, lets you select a source language, or lets you enter a custom language name.
- Saves transcript outputs as `.txt` and, optionally, `.xlsx`.
- Saves outputs next to the input files by default, with an option to use a custom output directory.
- Can download one ZIP archive when transcription completes; the uncompressed outputs remain in the output folder.
- Can optionally split long extracted audio into fixed-length segments before transcription.
- Shows transcription progress in the Gradio Status panel while work is running.

Usage instructions are included in `Whisper_v3.ipynb`.

When you open the notebook in Colab, click the play button on the `Launch Whisper Colab App` cell. The cell prints a temporary Gradio URL. Open it in a new tab, pick recordings from Google Drive, then run transcription in the app.

The notebook metadata requests a GPU runtime, and the launch cell requires a CUDA GPU by default. If Colab still opens a CPU runtime, choose `Runtime > Change runtime type > Hardware accelerator > GPU`, then rerun the launch cell.

The Gradio share URL is public while the app is running. The app allows Gradio to serve files under `/content/drive/MyDrive`, the output directory, and a temporary ZIP download directory so picker and download features can work. Avoid confidential recordings when using a public share URL.

If `MOUNT_GOOGLE_DRIVE` is disabled or Drive is unavailable, the app hides Drive input modes and leaves only local upload mode available. Upload mode starts transcription automatically after upload completes; the file component shows native upload progress, and the app reports uploaded file sizes once the upload reaches 100%.

By default, transcript files are saved in the same folder as each input file. Uploaded local files are saved under `/content/whisper_outputs` because uploads live in a temporary Colab location. Enable the custom output directory option only when you want all transcript files saved in one folder.

If download on completion is enabled, the app downloads one ZIP archive. Browsers can ask for confirmation when a page starts multiple downloads, so this app does not auto-download individual files.

`Search Drive folders recursively` controls folder modes. When it is enabled, the app scans selected or typed folders and their subfolders. When it is disabled, only files directly inside each selected or typed folder are used.

Colab can still disconnect an idle runtime. A running transcription uses compute and should not count as idle in the same way, but leaving the Gradio app open without work does not guarantee that Colab will keep the runtime alive indefinitely.

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
- The Drive file picker is filtered toward files, and the Drive folder picker is filtered toward folders, but Gradio may still allow unusual selections in some versions. The app validates selections before transcription and rejects folders in file mode, files in folder mode, and unsupported media extensions.
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

### No GPU is available

Enable a GPU runtime in Colab, then rerun the launch cell. The notebook requests GPU through metadata and exits before loading Whisper when `REQUIRE_GPU` is enabled but CUDA is unavailable.

### Gradio app URL does not appear

Keep `INSTALL_PACKAGES` enabled and rerun the launch cell. If Drive authorization is shown, complete it before opening the Gradio URL.

## Local tests

```powershell
python scripts/build_notebook.py --check
ruff format --check .
ruff check .
python -m unittest
```

The same checks run in GitHub Actions on pushes to `main` and on pull requests.
