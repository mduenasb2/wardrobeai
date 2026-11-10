# WardrobeAI — PC reconstruction

This folder contains a local browser-based reconstruction of WardrobeAI's Android try-on workflow, its tests and its analysis record. The original Android project remains under `../` and was not edited.

## Run

Requirements: Python 3.10+; no pip packages, Android SDK or system-wide installation is needed.

```bash
cd wardrobeai/source-migration/app
python3 server.py
```

Open <http://127.0.0.1:8765/>. Select a person photo, select a clothing image, then choose **Try on this look**. With no credential configured, the app creates the same fixed-position local composite as the Android fallback and does not upload photos. The result can be downloaded as PNG. **Try another outfit** keeps the person photo and clears the garment and result.

Optional Gemini generation requires a valid Gemini API key in the server environment. Keep it out of source files and shell history; for example, set `GEMINI_API_KEY` in a private environment manager before launching `python3 server.py`. The server sends the two resized photos to Google's Gemini API only when that key is present. The app tries the configured model sequence and falls back to the local composite if Gemini cannot return an image. The key remains server-side.

The server binds to loopback (`127.0.0.1`), and images/state are held in browser memory for the session. No selected input is written to the project. `WARDROBEAI_PORT` can select another local port if 8765 is occupied.

## Tests

From `wardrobeai/source-migration/` run:

```bash
python3 -m unittest discover -s tests -v
```

See [`docs/SOURCE_ANALYSIS.md`](docs/SOURCE_ANALYSIS.md), [`docs/REQUIREMENTS.md`](docs/REQUIREMENTS.md), [`docs/PARITY_REPORT.md`](docs/PARITY_REPORT.md) and [`evidence/EVIDENCE_INDEX.md`](evidence/EVIDENCE_INDEX.md) for behavior and traceability.
