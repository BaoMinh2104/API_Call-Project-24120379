from pydantic import BaseModel, Field


class CaptionResponse(BaseModel):
    model: str = Field(..., description="Tên model đang được sử dụng")
    filename: str = Field(..., description="Tên file ảnh đã tải lên")
    content_type: str = Field(..., description="Kiểu MIME của file")
    prompt: str | None = Field(default=None, description="Prompt điều kiện nếu người dùng nhập")
    caption: str = Field(..., description="Mô tả ảnh được model sinh ra")
