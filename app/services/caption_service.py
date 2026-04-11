from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO

import torch
from PIL import Image, UnidentifiedImageError
from transformers import BlipForConditionalGeneration, BlipProcessor


@dataclass(frozen=True)
class CaptionConfig:
    max_new_tokens: int = 50
    num_beams: int = 4


class CaptionService:
    def __init__(
        self,
        model_name: str = "Salesforce/blip-image-captioning-large",
        config: CaptionConfig | None = None,
    ) -> None:
        self.model_name = model_name
        self.config = config or CaptionConfig()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.dtype = torch.float16 if self.device == "cuda" else torch.float32
        self._processor: BlipProcessor | None = None
        self._model: BlipForConditionalGeneration | None = None

    def _load_model(self) -> None:
        if self._processor is not None and self._model is not None:
            return

        self._processor = BlipProcessor.from_pretrained(self.model_name)
        self._model = BlipForConditionalGeneration.from_pretrained(
            self.model_name,
            torch_dtype=self.dtype,
        )
        self._model.to(self.device)
        self._model.eval()

    def is_ready(self) -> bool:
        return self._processor is not None and self._model is not None

    def get_model_name(self) -> str:
        return self.model_name

    def get_device(self) -> str:
        return self.device

    def _prepare_image(self, image_bytes: bytes) -> Image.Image:
        try:
            image = Image.open(BytesIO(image_bytes)).convert("RGB")
        except UnidentifiedImageError as exc:
            raise ValueError("Không thể đọc file ảnh. Hãy tải lên ảnh hợp lệ.") from exc
        except OSError as exc:
            raise ValueError("File ảnh bị lỗi hoặc định dạng không được hỗ trợ.") from exc
        return image

    def _move_inputs_to_device(self, inputs):
        moved_inputs = {}
        for key, value in inputs.items():
            if torch.is_tensor(value):
                if torch.is_floating_point(value):
                    moved_inputs[key] = value.to(self.device, self.dtype)
                else:
                    moved_inputs[key] = value.to(self.device)
            else:
                moved_inputs[key] = value
        return moved_inputs

    def generate_caption(self, image_bytes: bytes, prompt: str | None = None) -> str:
        if not image_bytes:
            raise ValueError("File ảnh rỗng.")

        self._load_model()
        image = self._prepare_image(image_bytes)
        cleaned_prompt = prompt.strip() if prompt else ""

        if cleaned_prompt:
            inputs = self._processor(image, cleaned_prompt, return_tensors="pt")
        else:
            inputs = self._processor(image, return_tensors="pt")

        inputs = self._move_inputs_to_device(inputs)

        with torch.no_grad():
            outputs = self._model.generate(
                **inputs,
                max_new_tokens=self.config.max_new_tokens,
                num_beams=self.config.num_beams,
            )

        result = self._processor.decode(outputs[0], skip_special_tokens=True).strip()
        if not result:
            raise RuntimeError("Model không tạo được caption cho ảnh này.")
        return result


caption_service = CaptionService()
