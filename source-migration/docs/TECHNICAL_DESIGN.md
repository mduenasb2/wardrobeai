# Technical design

## Selected technology

**Python 3.10+ standard library for a loopback server, with browser-native HTML, CSS and JavaScript for the user interface and Canvas image composition.** No pip package manager or system installation is required. This keeps local launch straightforward and avoids all Android APIs.

The choice is an implementation decision for the PC version. Discovered behavior is the two-image try-on workflow, validation, optional Gemini API, fallback image composition, save/export and repeat flow (`ev_86373d7242459e9ae719845a889be84fb7c7ebfd1e6681e4740f48d72151b9b5`, `ev_8d16e59edeaee7e4c236258caa6cc017f8a08fd57f605e9e14240b5ccc64f48a`, `ev_6563e4ebbe1d21ccf2c19af9a2988fda875f93f3adb0a0a270af097e43d57b51`, `src_ev_wardrobeai_screen_flow_001`). Use of Python, a loopback server and browser-native Canvas are new design choices.

## Components and data flow

* `app/server.py` serves three static assets and two same-origin endpoints (`/api/health`, `/api/try-on`) on `127.0.0.1`. It validates request shape, image MIME/data URL, base64 and size. It does not log request content or filenames.
* `app/static/index.html` and `styles.css` form the responsive single-page input/result experience.
* `app/static/app.js` holds person/garment selection and result only in page memory; it resizes chosen images to a 1024 px maximum dimension, previews them, sends their JPEG data URLs to the local API, or draws the local fallback on Canvas. The user explicitly downloads the result.
* `app/gemini.py` is used only if `GEMINI_API_KEY` is present in the server process. It builds the discovered prompt and two-image payload, sends HTTPS requests in source model order, parses the first image part and returns a data URL. Failed/text-only attempts fall back to the local composite.

Without a key, `/api/try-on` validates the request but returns `mode=composite`; the local browser creates the preview. No image goes to an external service in this mode. With a key, the server forwards the resized photos to Google Gemini. Credentials stay in server environment rather than the browser package. This boundary is a PC security design choice; the Android source obtains a generated BuildConfig field from local properties (`src_ev_wardrobeai_build_configuration_001`).

## Image processing and storage

The browser decodes each selected image and scales it proportionally so the longest side is at most 1024 px, reflecting the source's `loadSampledBitmap(..., 1024)` argument (`src_ev_wardrobeai_image_loading_001`). Local composition creates a canvas equal to the person-image dimensions, draws the person, then draws the garment rectangle centered at 68% of person width and 28% from the top (`ev_6563e4ebbe1d21ccf2c19af9a2988fda875f93f3adb0a0a270af097e43d57b51`). Browser Canvas is an approximation of Android `Bitmap`/`Canvas`; exact resampling may differ. No segmentation or geometry improvements are introduced.

The only persistent output is the PNG the user downloads. Input data URLs and result remain in browser memory. The web app introduces no database, account, remote storage or background worker. Browser download destination replaces the Android MediaStore location; the original PNG export behavior is supported by `src_ev_wardrobeai_save_image_001` and `ev_db2517940eb9dc91b97eb9159bc91ae0dd8028f4d4fb7c40bbad939e77cff097`.

## Configuration and operation

Run `python3 app/server.py` from `wardrobeai/source-migration/` (or `python3 server.py` from `app/`). `WARDROBEAI_PORT` optionally selects another loopback port. Without `GEMINI_API_KEY`, local generation is fully offline. With a key, Gemini calls are enabled; the PC copy never defaults to a committed key. There is no packaging/build stage and no Android/Gemini SDK dependency.

## Error handling

Client input decoding and server input validation show actionable UI errors. The server caps each decoded image to 8 MiB and a JSON request to 24 MiB. API errors and text-only responses do not leak raw response bodies; model attempts continue and then local preview is shown. Network image-generation quality, model eligibility and service costs cannot be verified without an actual configured API key and request.
