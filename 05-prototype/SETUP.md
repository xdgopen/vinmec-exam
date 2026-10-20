# Hướng dẫn cài đặt và chạy prototype

| Thông tin | |
|---|---|
| Ứng dụng | Prototype đặt lịch tái khám hộ người thân (Streamlit, dữ liệu giả) |
| Phiên bản | 0.2.0 |
| Đã kiểm tra | Cách A (Python): macOS, Python 3.13 và 3.14, cài bằng `pip` và `uv`, 18/18 test qua, app khởi động bình thường (bản 0.2.0, 20/10/2026). Cách B (Docker): image `python:3.13-slim`, khoảng 840 MB, container ở trạng thái `healthy`, chạy bằng user thường, 4 tình huống thử bằng lệnh trong container đều đúng (20/10/2026) |
| Thuật ngữ | Xem `../THUAT-NGU.md` |

Prototype chạy được cả khi không có API key. Khi đó app dùng bộ đọc theo luật (chế độ không dùng AI). API key chỉ cần nếu muốn bật phần AI đọc câu nhập tự do.

## 1. Chọn cách chạy

| | Cách A: Python | Cách B: Docker |
|---|---|---|
| Cần cài | Python 3.10 trở lên | Docker Desktop |
| Lệnh chạy | `streamlit run app.py` | `docker compose up --build` |
| Chạy được test | Có | Không (image chỉ chứa phần chạy app) |
| Hợp khi | Muốn sửa code, chạy test | Máy không có Python, muốn chạy giống nhau trên mọi máy |

Cả hai cách đều mở app tại `http://localhost:8501`. Mọi lệnh đều chạy **trong thư mục `05-prototype/`**.

## 2. Cách A: chạy bằng Python

**Cài đặt trên macOS, Linux**

```bash
cd 05-prototype
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

**Cài đặt trên Windows (PowerShell)**

```powershell
cd 05-prototype
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

Nếu PowerShell báo không được chạy script, hãy chạy `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` một lần rồi kích hoạt lại môi trường ảo. Nếu đã có `uv`, có thể cài nhanh hơn bằng `uv venv && uv pip install -r requirements-dev.txt`.

`requirements.txt` gồm thư viện để chạy app (streamlit, anthropic). `requirements-dev.txt` có thêm pytest để chạy test.

**Chạy app**

```bash
streamlit run app.py
```

Trình duyệt tự mở `http://localhost:8501`. Nếu không tự mở, hãy dán địa chỉ đó vào trình duyệt. Dừng app bằng `Ctrl + C`.

## 3. Cách B: chạy bằng Docker

**Docker Compose (gọn nhất)**

```bash
cd 05-prototype
docker compose up --build
```

Dừng bằng `Ctrl + C`, rồi chạy `docker compose down`.

**Lệnh Docker thường**

```bash
cd 05-prototype
docker build -t vinmec-tai-kham-prototype:0.2.0 .
docker run --rm -p 8501:8501 vinmec-tai-kham-prototype:0.2.0
```

Một số điều cần biết:
- **Lần build đầu** phải tải khoảng 100 MB thư viện từ PyPI. Mạng chậm thì có thể mất từ vài phút đến hơn nửa giờ. Các lần build sau dùng cache nên nhanh hơn nhiều.
- **Image chỉ chứa phần cần để chạy app:** `app.py`, `core.py`, `mock-data/`, `prompts/`. Không có test, tài liệu hay ảnh chụp.
- **App trong container** chạy bằng user thường (không dùng root), có healthcheck tại `/_stcore/health`. Lệnh `docker ps` sẽ hiện trạng thái `healthy` khi app sẵn sàng.

## 4. Bật AI (tùy chọn, chưa kiểm chứng)

Bản hiện tại chạy bằng luật và **chưa bật AI**. Phần dưới mô tả cách bật khi muốn thử. Việc gọi AI thật chưa được kiểm chứng trong bài tập này.

Nhãn "Chế độ không dùng AI" ở góc màn hình nghĩa là app chưa có API key. Mọi luồng vẫn chạy bình thường. Muốn bật AI, hãy lấy key tại console.anthropic.com rồi làm theo cách chạy bạn đang dùng.

| Cách chạy | Cách đưa key vào |
|---|---|
| Cách A, dùng file | `cp .streamlit/secrets.toml.example .streamlit/secrets.toml`, mở file và điền `ANTHROPIC_API_KEY = "sk-ant-..."` |
| Cách A, dùng biến môi trường | `export ANTHROPIC_API_KEY="sk-ant-..."` (Windows: `$env:ANTHROPIC_API_KEY="sk-ant-..."`), rồi chạy lại `streamlit run app.py` |
| Cách B, Compose | Đặt biến môi trường như trên, rồi chạy `docker compose up --build` |
| Cách B, lệnh Docker | `docker run --rm -p 8501:8501 -e ANTHROPIC_API_KEY="sk-ant-..." vinmec-tai-kham-prototype:0.2.0` |

Lưu ý về key:
- **Không commit key.** `.streamlit/secrets.toml` và `.env` đã nằm trong `.gitignore`.
- **Key không nằm trong image Docker.** `.dockerignore` chặn `.streamlit/` và `.env`. Key chỉ được truyền lúc chạy, qua biến môi trường.
- File `secrets.toml` chỉ được đọc khi chạy lệnh **từ trong `05-prototype/`**.
- Nếu gọi AI lỗi (sai key, hết hạn mức, lỗi mạng), app tự chuyển sang chế độ không dùng AI, không bị dừng.

## 5. Kiểm tra sau khi cài

**Test tự động (chỉ với cách A)**

```bash
python -m pytest -q tests
```

Kết quả đúng là `18 passed`. Trong test, AI được giả lập, nên không cần key.

**Thử tay 4 tình huống (cả hai cách)**

| # | Thao tác | Kết quả đúng |
|---|---|---|
| 1 | Ở phiếu tái khám PT-001, bấm "Xem lịch trống và đặt" | Hiện nhiều ngày trống của bác sĩ Trần Minh An cùng lúc. Chọn một giờ thì sang màn hình xác nhận |
| 2 | Gõ `đặt tái khám cho mẹ với bác sĩ An giữa tháng 11` rồi bấm "Tìm lịch" | Tìm được bác sĩ Trần Minh An khi chỉ gõ tên gọi |
| 3 | Gõ `đặt tái khám cho bố với bác sĩ Nguyễn Thanh David` | Báo "Không tìm thấy" và không tự đoán bác sĩ |
| 4 | Gõ `bố tôi đột nhiên đau ngực, khó thở` | Hiện ngay khung cấp cứu và nút "Gọi 115". Không cho đặt lịch |
| 5 | Ở mục "Tạo phiếu từ giấy hẹn", bấm "Mẫu GH-2" rồi "Tạo phiếu tái khám" | Màn hình kiểm tra hiện bác sĩ Lê Thu Hà, ngày hẹn 20/11/2026, báo đã bỏ 2 dòng thông tin cá nhân. Bấm "Đúng, tạo phiếu…" thì sang lịch trống |
| 6 | Bấm "Mẫu GH-3" rồi "Tạo phiếu tái khám" (không có API key) | Nhãn "Chế độ không dùng AI", báo chưa đọc được ngày hẹn và cho người dùng tự chọn. Có key thì AI đọc được ngày hẹn |

## 6. Đưa lên mạng để có link (Streamlit Community Cloud)

1. Đẩy repo lên GitHub.
2. Vào share.streamlit.io, đăng nhập bằng GitHub, chọn **Create app**.
3. Chọn repo và nhánh. Ở mục *Main file path* điền `05-prototype/app.py`.
4. Nếu muốn bật AI: vào *Advanced settings*, phần *Secrets*, dán `ANTHROPIC_API_KEY = "sk-ant-..."`.
5. Bấm **Deploy**. Sau vài phút sẽ có link dạng `https://<tên-app>.streamlit.app`. Dán link này vào README.

## 7. Lỗi thường gặp

| Lỗi | Nguyên nhân | Cách xử lý |
|---|---|---|
| `streamlit: command not found` | Chưa kích hoạt môi trường ảo | Chạy lại `source .venv/bin/activate` (Windows: `.venv\Scripts\Activate.ps1`), hoặc dùng `python -m streamlit run app.py` |
| `ModuleNotFoundError: streamlit` hoặc `anthropic` | Chưa cài thư viện, hoặc cài vào Python khác | Kích hoạt môi trường ảo rồi chạy lại `pip install -r requirements-dev.txt` |
| `Port 8501 is already in use`, hoặc Docker báo `port is already allocated` | Cổng 8501 đang bị dùng | Cách A: `streamlit run app.py --server.port 8502`. Cách B: đổi cổng bên trái, ví dụ `-p 8502:8501` (hoặc `"8502:8501"` trong `docker-compose.yml`), rồi mở `http://localhost:8502` |
| `Cannot connect to the Docker daemon` | Docker Desktop chưa chạy | Mở Docker Desktop, đợi biểu tượng báo đang chạy rồi thử lại |
| Build Docker dừng ở `pip install` hoặc báo lỗi mạng | Mạng chậm hoặc bị chặn khi tải thư viện từ PyPI | Chạy lại lệnh build. Các gói đã tải xong sẽ không phải tải lại nếu bước đó đã hoàn tất |
| Đã điền key mà vẫn hiện "Chế độ không dùng AI" | Key sai, hết hạn mức, model không truy cập được, hoặc key chưa được đưa vào đúng chỗ | Kiểm tra lại theo bảng ở mục 4. Với Docker, key phải được truyền bằng `-e` hoặc biến môi trường trước khi chạy Compose |
| Trình duyệt không tự mở | Chạy trên máy chủ, chế độ headless hoặc Docker | Mở thủ công `http://localhost:8501` |

## 8. Cấu trúc thư mục

```
05-prototype/
├── app.py                     giao diện Streamlit
├── core.py                    logic: kiểm tra khẩn cấp, đọc yêu cầu, tìm bác sĩ, lịch trống
├── mock-data/                 dữ liệu giả: bác sĩ, lịch trống, phiếu tái khám, giấy hẹn mẫu
├── prompts/                   system prompt cho AI: đọc yêu cầu, đọc giấy hẹn
├── tests/test_app.py          18 test tự động
├── requirements.txt           thư viện để chạy app
├── requirements-dev.txt       thêm pytest để chạy test
├── Dockerfile                 đóng gói app thành image Docker
├── docker-compose.yml         chạy image bằng một lệnh
├── .dockerignore              loại test, tài liệu, key khỏi image
├── .streamlit/secrets.toml.example   mẫu file key (không chứa key thật)
├── SETUP.md                   hướng dẫn này
├── README.md                  mô tả prototype và guardrail
├── test-log.md                nhật ký thử với người dùng
└── CHANGELOG.md               nhật ký thay đổi
```
