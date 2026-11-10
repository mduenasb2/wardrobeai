"""Local HTTP/API boundary for the WardrobeAI PC reconstruction."""

from __future__ import annotations

import base64
import binascii
import json
import os
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

from gemini import request_gemini_image


ROOT = Path(__file__).resolve().parent
STATIC_ROOT = ROOT / "static"
MAX_REQUEST_BYTES = 24 * 1024 * 1024
MAX_IMAGE_BYTES = 8 * 1024 * 1024
IMAGE_DATA_URL = re.compile(r"^data:image/(?:jpeg|png|webp);base64,([A-Za-z0-9+/]+={0,2})$")


class RequestError(ValueError):
    """A request did not match the supported local API contract."""


def decode_image_data_url(value: object) -> tuple[str, bytes]:
    if not isinstance(value, str):
        raise RequestError("Each selected file must be an image.")
    match = IMAGE_DATA_URL.fullmatch(value)
    if match is None:
        raise RequestError("Use a JPEG, PNG, or WebP image.")
    try:
        image_bytes = base64.b64decode(match.group(1), validate=True)
    except (binascii.Error, ValueError) as error:
        raise RequestError("The selected image could not be decoded.") from error
    if not image_bytes:
        raise RequestError("The selected image is empty.")
    if len(image_bytes) > MAX_IMAGE_BYTES:
        raise RequestError("Each image must be 8 MB or smaller after resizing.")
    return value.partition(",")[0].removeprefix("data:").removesuffix(";base64"), image_bytes


def create_generation_response(payload: object, api_key: str | None = None) -> dict[str, str]:
    if not isinstance(payload, dict):
        raise RequestError("The request must contain an image object.")
    person_mime, person_bytes = decode_image_data_url(payload.get("person"))
    garment_mime, garment_bytes = decode_image_data_url(payload.get("garment"))

    key = (api_key if api_key is not None else os.environ.get("GEMINI_API_KEY", "")).strip()
    if not key:
        return {"mode": "composite"}

    generated = request_gemini_image(key, person_mime, person_bytes, garment_mime, garment_bytes)
    if generated is None:
        return {"mode": "composite", "message": "Gemini did not return an image; showing the local preview instead."}
    return {"mode": "gemini", "image": generated}


class WardrobeHandler(BaseHTTPRequestHandler):
    server_version = "WardrobeAI/1.0"

    def log_message(self, _format: str, *_args: object) -> None:
        # Keep image names, prompt payloads and API response details out of logs.
        return

    def _send_json(self, status: int, value: dict[str, object]) -> None:
        content = json.dumps(value).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        path = unquote(urlsplit(self.path).path)
        if path == "/api/health":
            self._send_json(200, {"gemini_available": bool(os.environ.get("GEMINI_API_KEY", "").strip())})
            return

        file_name = "index.html" if path in ("/", "/index.html") else path.lstrip("/")
        if file_name not in {"index.html", "app.js", "styles.css"}:
            self._send_json(404, {"error": "Not found."})
            return
        file_path = STATIC_ROOT / file_name
        content = file_path.read_bytes()
        content_type = "text/html; charset=utf-8" if file_name.endswith(".html") else (
            "text/javascript; charset=utf-8" if file_name.endswith(".js") else "text/css; charset=utf-8"
        )
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        if urlsplit(self.path).path != "/api/try-on":
            self._send_json(404, {"error": "Not found."})
            return
        try:
            length = int(self.headers.get("Content-Length", "-1"))
        except ValueError:
            length = -1
        if length < 0 or length > MAX_REQUEST_BYTES:
            self._send_json(413, {"error": "The selected images exceed the request size limit."})
            return
        try:
            payload = json.loads(self.rfile.read(length))
            response = create_generation_response(payload)
        except (json.JSONDecodeError, RequestError) as error:
            self._send_json(400, {"error": str(error)})
            return
        except Exception:
            self._send_json(502, {"error": "Image generation failed. Please try again."})
            return
        self._send_json(200, response)


def main() -> None:
    address = ("127.0.0.1", int(os.environ.get("WARDROBEAI_PORT", "8765")))
    server = ThreadingHTTPServer(address, WardrobeHandler)
    print(f"WardrobeAI is ready at http://{address[0]}:{address[1]}/ (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nWardrobeAI stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
