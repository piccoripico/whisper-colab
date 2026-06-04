# whisper-colab

A thin Google Colab notebook for transcribing audio and video files with Whisper.

[Open in Colab](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/Whisper_v3.ipynb)

## What this repository does

- Keeps the notebook small: user settings stay in the notebook, while the workflow lives in `src/whisper_colab`.
- Converts input audio or video to Whisper-friendly WAV before transcription.
- Uses `16 kHz / mono / PCM WAV` extraction through `ffmpeg`.
- Downloads transcript outputs as `.txt` and, optionally, `.xlsx`.

## Colab usage

1. Open `Whisper_v3.ipynb` in Google Colab.
2. Edit the settings cell.
3. Run the bootstrap/run cell.
4. Choose files through Colab upload, or set Google Drive paths when `USE_GOOGLE_DRIVE_FILES` is enabled.

The notebook clones this repository from:

```text
https://github.com/piccoripico/whisper-colab.git
```

## Generated notebook

`Whisper_v3.ipynb` is generated from `scripts/build_notebook.py`. Edit the script, then rebuild the notebook:

```powershell
python scripts/build_notebook.py
```

## Known limitations

- Whisper can hallucinate common phrases during silence, especially at the beginning of recordings. This repository does not remove those phrases in post-processing.
- Very long recordings may fail when the Colab runtime runs out of GPU or system memory.
- `ffmpeg` must be available. It is normally available in Colab, and the runner installs it when needed.

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
