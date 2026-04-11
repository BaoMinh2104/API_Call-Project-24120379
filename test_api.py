import io
import os

import pytest
import requests
from PIL import Image

BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
TIMEOUT = 180
MODEL_NAME = "Salesforce/blip-image-captioning-large"


def call_api(method: str, path: str, **kwargs) -> requests.Response:
    url = f"{BASE_URL}{path}"
    try:
        return requests.request(method, url, timeout=TIMEOUT, **kwargs)
    except requests.RequestException as exc:
        pytest.fail(
            f"Không thể kết nối API tại {url}. "
            f"Hãy chạy uvicorn trước khi test. Chi tiết: {exc}"
        )


def make_test_image_bytes() -> bytes:
    image = Image.new("RGB", (64, 64), color="white")
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def test_root() -> None:
    response = call_api("GET", "/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "BLIP Image Captioning API"
    assert data["model"] == MODEL_NAME
    assert "/caption" in data["endpoints"]


def test_health() -> None:
    response = call_api("GET", "/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["model"] == MODEL_NAME
    assert data["device"] in {"cpu", "cuda"}


def test_caption_reject_non_image_file() -> None:
    response = call_api(
        "POST",
        "/caption",
        files={"file": ("note.txt", b"hello", "text/plain")},
    )
    assert response.status_code == 400
    assert "ảnh hợp lệ" in response.json()["detail"]


def test_caption_valid_image() -> None:
    image_bytes = make_test_image_bytes()
    response = call_api(
        "POST",
        "/caption",
        data={"prompt": "a photography of"},
        files={"file": ("test.png", image_bytes, "image/png")},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["model"] == MODEL_NAME
    assert data["filename"] == "test.png"
    assert data["content_type"] == "image/png"
    assert data["prompt"] == "a photography of"
    assert isinstance(data["caption"], str)
    assert data["caption"].strip() != ""
