from __future__ import annotations

import base64
import json
import sys
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from server import RequestError, WardrobeHandler, create_generation_response, decode_image_data_url  # noqa: E402
from gemini import FALLBACK_MODELS, TRYON_PROMPT, request_gemini_image  # noqa: E402


PNG_BYTES = b"\x89PNG\r\n\x1a\nfixture"
PNG_DATA_URL = "data:image/png;base64," + base64.b64encode(PNG_BYTES).decode("ascii")


class Response:
    def __init__(self, value: object):
        self.value = value

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return json.dumps(self.value).encode("utf-8")


class WardrobeServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), WardrobeHandler)
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.httpd.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.thread.join(timeout=2)

    def test_home_and_health_are_served_locally(self):
        with urlopen(self.base_url + "/") as response:
            self.assertEqual(response.status, 200)
            self.assertIn(b"WardrobeAI", response.read())
        with urlopen(self.base_url + "/api/health") as response:
            self.assertEqual(json.loads(response.read()), {"gemini_available": False})

    def test_no_key_selects_local_composite_without_network(self):
        self.assertEqual(
            create_generation_response({"person": PNG_DATA_URL, "garment": PNG_DATA_URL}, api_key=""),
            {"mode": "composite"},
        )

    def test_rejects_missing_or_malformed_images(self):
        with self.assertRaises(RequestError):
            decode_image_data_url("not an image")
        with self.assertRaises(RequestError):
            create_generation_response({"person": PNG_DATA_URL}, api_key="")

    def test_api_returns_client_error_for_invalid_image(self):
        body = json.dumps({"person": "bad", "garment": PNG_DATA_URL}).encode()
        request = Request(self.base_url + "/api/try-on", data=body, headers={"Content-Type": "application/json"})
        with self.assertRaises(HTTPError) as raised:
            urlopen(request)
        self.assertEqual(raised.exception.code, 400)
        error_body = raised.exception.read().decode().lower()
        raised.exception.close()
        self.assertIn("image", error_body)

    def test_gemini_request_uses_two_images_and_returns_image_part(self):
        captured = []
        image = base64.b64encode(PNG_BYTES).decode("ascii")

        def opener(request, timeout):
            captured.append((request, timeout))
            return Response({"candidates": [{"content": {"parts": [
                {"text": "generated"}, {"inlineData": {"mimeType": "image/png", "data": image}},
            ]}}]})

        result = request_gemini_image("local-test-key", "image/png", PNG_BYTES, "image/png", PNG_BYTES, opener)
        self.assertEqual(result, "data:image/png;base64," + image)
        request, timeout = captured[0]
        body = json.loads(request.data)
        self.assertEqual(timeout, 90)
        self.assertEqual(request.get_method(), "POST")
        self.assertIn("key=local-test-key", request.full_url)
        parts = body["contents"][0]["parts"]
        self.assertEqual(parts[0]["text"], TRYON_PROMPT)
        self.assertEqual(len([part for part in parts if "inlineData" in part]), 2)
        self.assertEqual(body["generationConfig"]["responseModalities"], ["IMAGE", "TEXT"])

    def test_gemini_fallbacks_are_exhausted_when_no_image_is_returned(self):
        attempted = []

        def opener(request, timeout):
            attempted.append(request.full_url)
            return Response({"candidates": [{"content": {"parts": [{"text": "not an image"}]}}]})

        self.assertIsNone(request_gemini_image("key", "image/png", PNG_BYTES, "image/png", PNG_BYTES, opener))
        self.assertEqual(len(attempted), len(FALLBACK_MODELS))
        for model, url in zip(FALLBACK_MODELS, attempted):
            self.assertIn(model, url)


if __name__ == "__main__":
    unittest.main()
