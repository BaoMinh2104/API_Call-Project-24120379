# BLIP Image Captioning API

## 1. Thông tin sinh viên

- Họ và tên: `Chu Bảo Minh`
- MSSV: `24120379`
- Lớp: `24CTT4`
- Lớp TDTT: `24CTT3`

## 2. Tên mô hình và link mô hình trên Hugging Face

- Model sử dụng: `Salesforce/blip-image-captioning-large`
- Link model: `https://huggingface.co/Salesforce/blip-image-captioning-large`

## 3. Mô tả tương quan về chức năng của hệ thống

Project này xây dựng một hệ thống API tạo mô tả ảnh bằng FastAPI.
API nhận file ảnh người dùng tải lên, gọi mô hình BLIP từ Hugging Face thông qua thư viện Transformers và trả về caption dưới dạng JSON.

Ngoài chế độ caption thông thường, API còn hỗ trợ nhập thêm `prompt` để tạo caption có điều kiện.
Ví dụ, có thể truyền prompt như `a photography of` để định hướng câu mô tả sinh ra từ model.

## 4. Cấu trúc thư mục

```text
blip_api_project/
├─ app/
│  ├─ main.py
│  ├─ schemas.py
│  └─ services/
│     └─ caption_service.py
├─ requirements.txt
├─ README.md
└─ test_api.py
```

## 5. Hướng dẫn cài đặt

Tạo môi trường ảo, kích hoạt môi trường và cài đặt các thư viện cần thiết:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 6. Hướng dẫn chạy chương trình

Chạy API:

```bash
uvicorn app.main:app --reload
```

Sau khi chạy có thể mở các địa chỉ để kiểm tra:

- API: `http://127.0.0.1:8000`
- Docs: `http://127.0.0.1:8000/docs`

Chạy test API:

```bash
pytest test_api.py -v
```

## 7. Hướng dẫn gọi API và ví dụ request/response

### GET /

```bash
curl http://127.0.0.1:8000/
```

### GET /health

```bash
curl http://127.0.0.1:8000/health
```

### POST /caption

Có 2 cách test:

### Cách 1: Dùng curl

```bash
curl -X POST "http://127.0.0.1:8000/caption" ^
  -F "file=@demo.jpg" ^
  -F "prompt=a photography of"
```

### Cách 2: Dùng `/docs`

- Mở `http://127.0.0.1:8000/docs`
- Chọn endpoint `POST /caption`
- Bấm `Try it out`
- Chọn file ảnh ở trường `file`
- Có thể nhập thêm `prompt` hoặc để trống
- Bấm `Execute`

Ví dụ response:

```json
{
  "model": "Salesforce/blip-image-captioning-large",
  "filename": "demo.jpg",
  "content_type": "image/jpeg",
  "prompt": "a photography of",
  "caption": "a photography of a dog sitting on the grass"
}
```

Nếu file không phải ảnh, API trả về `400`.
Nếu model lỗi, API trả về `500`.

## 8. Hướng dẫn dùng Pinggy để demo public

Sau khi API đang chạy ở `localhost:8000`, mở một terminal khác và chạy lệnh sau:

```bash
ssh -p 443 -R0:127.0.0.1:8000 free.pinggy.io
```

Pinggy sẽ cung cấp một đường dẫn public để truy cập từ Internet.
Ví dụ có thể dùng link dạng:

```text
https://xxxxx.pinggy.link/docs
```
=======
