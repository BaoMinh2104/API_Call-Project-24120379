from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from app.schemas import CaptionResponse
from app.services.caption_service import caption_service

app = FastAPI(title="BLIP Image Captioning API", version="1.0.0")


@app.get("/")
def root():
    return {
        "name": "BLIP Image Captioning API",
        "model": caption_service.get_model_name(),
        "message": "API đang hoạt động.",
        "endpoints": ["/", "/health", "/caption"],
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": caption_service.get_model_name(),
        "device": caption_service.get_device(),
        "loaded": caption_service.is_ready(),
    }


@app.post("/caption", response_model=CaptionResponse)
async def caption_image(
    file: UploadFile = File(..., description="Ảnh cần tạo caption"),
    prompt: str | None = Form(default=None, description="Prompt tùy chọn, ví dụ: a photography of"),
):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File tải lên phải là ảnh hợp lệ.")

    try:
        image_bytes = await file.read()
        if not image_bytes:
            raise HTTPException(status_code=400, detail="File ảnh rỗng.")

        caption_text = caption_service.generate_caption(image_bytes=image_bytes, prompt=prompt)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi sinh caption từ model: {exc}",
        ) from exc

    return CaptionResponse(
        model=caption_service.get_model_name(),
        filename=file.filename or "uploaded_image",
        content_type=file.content_type,
        prompt=prompt.strip() if prompt and prompt.strip() else None,
        caption=caption_text,
    )
