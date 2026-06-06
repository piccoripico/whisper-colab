# Free Whisper Transcription on Google Colab, Without Per-Minute Limits

Run Whisper from a Google Colab notebook and transcribe audio or video files without paying per transcription minute. Usage is still bounded by Colab runtime availability, GPU access, and storage limits.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/Whisper_v3.ipynb)

## What It Does

- Launches a Gradio app from one Colab notebook.
- Uses Google Drive picker modes as the main input path.
- Falls back to upload-only input when Google Drive is not mounted.
- Converts audio or video to Whisper-friendly `16 kHz / mono / PCM WAV`.
- Runs `openai/whisper-large-v3-turbo` by default, with `openai/whisper-large-v3` also available.
- Saves transcripts as `.txt` and, optionally, `.xlsx`.
- Saves outputs next to the source files by default, or to a custom folder when enabled.
- Prepares one ZIP download when requested.
- Shows progress in the Gradio Status panel while transcription is running.

Usage instructions are included in `Whisper_v3.ipynb`. Open the notebook, choose `Runtime > Run all`, wait for the Gradio URL, then open the app. Keep the Colab notebook open while using the app.

## Notes

- The Gradio share URL is public while the app is running. Avoid confidential recordings when using a public share URL.
- A running transcription uses compute, but an idle Colab runtime can still disconnect.
- For Japanese or other known-language recordings, selecting the source language can improve stability and avoid language-detection mistakes.
- The WAV extraction step normalizes audio for Whisper and should not meaningfully reduce speech-recognition quality. It uses `16 kHz / mono / PCM WAV`, which is the expected Whisper input format.
- Very long recordings may fail when the Colab runtime runs out of GPU or system memory.
- Browser security may block automatic downloads. If the ZIP does not download automatically, use the ZIP download panel shown after processing.

## Generated Notebook

`Whisper_v3.ipynb` is generated from `scripts/build_notebook.py`. Edit the script, then rebuild the notebook:

```powershell
python scripts/build_notebook.py
```

## Local Checks

```powershell
python scripts/build_notebook.py --check
ruff format --check .
ruff check .
python -m unittest
```

The same checks run in GitHub Actions on pushes to `main` and on pull requests.
