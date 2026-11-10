"""Optional server-side Gemini image request; never exposes the key to the browser."""

from __future__ import annotations

import base64
import json
import urllib.error
import urllib.parse
import urllib.request


FALLBACK_MODELS = (
    "gemini-3.6-flash",
    "gemini-3.1-flash-image",
    "gemini-2.5-flash-image",
)
TRYON_PROMPT = """Create a realistic virtual try-on image.

Image 1 is the user's photo.
Image 2 is the clothing item the user wants to wear.

Put the clothing from Image 2 naturally onto the person in Image 1.

Requirements:
- Preserve the person's identity and face.
- Preserve the person's body proportions.
- Preserve the person's pose as much as possible.
- Make the clothing fit naturally on the person's body.
- Preserve the clothing's original color, pattern, material, and design.
- Make realistic folds, shadows, lighting, and fabric deformation.
- Do not change the person's face.
- Do not change the person's hairstyle unnecessarily.
- Do not add accessories unless they are present in the clothing image.
- Keep the background as close to the original user photo as possible.
- Produce a realistic photograph rather than an illustration."""


def _image_part(mime_type: str, data: bytes) -> dict[str, object]:
    return {"inlineData": {"mimeType": mime_type, "data": base64.b64encode(data).decode("ascii")}}


def _extract_image(response: dict[str, object]) -> str | None:
    candidates = response.get("candidates")
    if not isinstance(candidates, list) or not candidates or not isinstance(candidates[0], dict):
        return None
    content = candidates[0].get("content")
    if not isinstance(content, dict) or not isinstance(content.get("parts"), list):
        return None
    for part in content["parts"]:
        if not isinstance(part, dict) or not isinstance(part.get("inlineData"), dict):
            continue
        inline_data = part["inlineData"]
        mime_type = inline_data.get("mimeType")
        encoded = inline_data.get("data")
        if isinstance(mime_type, str) and mime_type.startswith("image/") and isinstance(encoded, str) and encoded:
            try:
                decoded = base64.b64decode(encoded, validate=True)
            except (ValueError, base64.binascii.Error):
                continue
            return f"data:{mime_type};base64,{base64.b64encode(decoded).decode('ascii')}"
    return None


def request_gemini_image(
    api_key: str,
    person_mime: str,
    person_bytes: bytes,
    garment_mime: str,
    garment_bytes: bytes,
    opener=None,
) -> str | None:
    if not api_key.strip():
        return None
    if opener is None:
        opener = urllib.request.urlopen

    request_json = {
        "contents": [{
            "role": "user",
            "parts": [
                {"text": TRYON_PROMPT},
                _image_part(person_mime, person_bytes),
                _image_part(garment_mime, garment_bytes),
            ],
        }],
        "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]},
    }
    body = json.dumps(request_json).encode("utf-8")

    for model in FALLBACK_MODELS:
        query = urllib.parse.urlencode({"key": api_key})
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?{query}"
        request = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST",
        )
        try:
            with opener(request, timeout=90) as response:
                decoded = json.loads(response.read())
            image = _extract_image(decoded)
            if image is not None:
                return image
        except (OSError, TimeoutError, urllib.error.URLError, ValueError, json.JSONDecodeError):
            continue
    return None
