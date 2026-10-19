# Hướng dẫn cài đặt và chạy prototype

| Thông tin | |
|---|---|
| Ứng dụng | Prototype đặt lịch tái khám hộ người thân (Streamlit, dữ liệu giả) |
| Phiên bản | 0.1.1 |
| Đã kiểm tra trên | macOS, Python 3.13 và 3.14, cài bằng `pip` và `uv`. Ngày 19/10/2026: 11/11 test qua, app khởi động bình thường |
| Thuật ngữ | Xem `../THUAT-NGU.md` |

Prototype chạy được ngay cả khi không có API key. Khi đó app dùng bộ đọc theo luật (chế độ không dùng AI). API key chỉ cần nếu muốn bật phần AI đọc câu nhập tự do.

## 1. Yêu cầu

| Thành phần | Ghi chú |
|---|---|
| Python 3.10 trở lên | Kiểm tra bằng `python3 --version` (Windows: `py --version`) |
| Kết nối mạng | Để tải thư viện lúc cài. Khi chạy chế độ không AI thì không cần mạng |
| API key của Anthropic (tùy chọn) | Lấy tại console.anthropic.com. Chỉ cần nếu muốn bật AI |

Thư viện cần cài nằm trong `requirements.txt` (streamlit, anthropic). Nếu muốn chạy test thì dùng `requirements-dev.txt`, file này có thêm pytest.

## 2. Cài đặt

Mọi lệnh đều chạy **trong thư mục `05-prototype/`**.

**macOS, Linux**

```bash
cd 05-prototype
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

**Windows (PowerShell)**

```powershell
cd 05-prototype
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

Nếu PowerShell báo không được chạy script, hãy chạy lệnh `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` một lần, rồi kích hoạt lại môi trường ảo.

Nếu đã có `uv`, có thể cài nhanh hơn bằng `uv venv && uv pip install -r requirements-dev.txt`.

## 3. Chạy app

```bash
streamlit run app.py
```

Trình duyệt sẽ tự mở `http://localhost:8501`. Nếu không tự mở, hãy dán địa chỉ đó vào trình duyệt. Muốn dừng app thì bấm `Ctrl + C` trong cửa sổ terminal.

Góc màn hình hiện nhãn **"Chế độ không dùng AI"** nghĩa là app chưa có API key. Mọi luồng vẫn chạy bình thường.

## 4. Bật AI (tùy chọn)

Có hai cách, chọn một:

**Cách 1: file secrets của Streamlit**

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Mở `.streamlit/secrets.toml` và điền key:

```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

**Cách 2: biến môi trường**

```bash
export ANTHROPIC_API_KEY="sk-ant-..."          # macOS, Linux
$env:ANTHROPIC_API_KEY="sk-ant-..."            # Windows PowerShell
```

Sau đó chạy lại `streamlit run app.py`. Lưu ý:
- File `secrets.toml` chỉ được đọc khi chạy lệnh **từ trong `05-prototype/`**.
- File này đã nằm trong `.gitignore`. Không commit key lên GitHub.
- Nếu gọi AI lỗi (sai key, hết hạn mức, lỗi mạng), app tự chuyển sang chế độ không dùng AI, không bị dừng.

## 5. Kiểm tra nhanh sau khi cài

**Chạy test tự động:**

```bash
python -m pytest -q tests
```

Kết quả đúng là `11 passed`. Test luôn chạy ở chế độ không dùng AI, nên không cần key.

**Thử tay 4 tình huống trên giao diện:**

| # | Thao tác | Kết quả đúng |
|---|---|---|
| 1 | Ở phiếu tái khám PT-001, bấm "Xem lịch trống và đặt" | Hiện nhiều ngày trống của bác sĩ Trần Minh An cùng lúc. Chọn một giờ thì sang màn hình xác nhận |
| 2 | Gõ `đặt tái khám cho mẹ với bác sĩ An giữa tháng 11` rồi bấm "Tìm lịch" | Tìm được bác sĩ Trần Minh An khi chỉ gõ tên gọi |
| 3 | Gõ `đặt tái khám cho bố với bác sĩ Nguyễn Thanh David` | Báo "Không tìm thấy" và không tự đoán bác sĩ |
| 4 | Gõ `bố tôi đột nhiên đau ngực, khó thở` | Hiện ngay khung cấp cứu và nút "Gọi 115". Không cho đặt lịch |

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
| `Port 8501 is already in use` | Đang có app Streamlit khác chạy | Tắt app đó, hoặc chạy `streamlit run app.py --server.port 8502` |
| Đã điền key mà vẫn hiện "Chế độ không dùng AI" | Key sai, hết hạn mức, tên model không truy cập được, hoặc `secrets.toml` không nằm trong `05-prototype/.streamlit/` | Kiểm tra key và vị trí file. Có thể thử bằng biến môi trường (mục 4, cách 2) |
| Trình duyệt không tự mở | Chạy trên máy chủ hoặc chế độ headless | Mở thủ công `http://localhost:8501` |

## 8. Cấu trúc thư mục

```
05-prototype/
├── app.py                     giao diện Streamlit
├── core.py                    logic: kiểm tra khẩn cấp, đọc yêu cầu, tìm bác sĩ, lịch trống
├── mock-data/                 dữ liệu giả: bác sĩ, lịch trống, phiếu tái khám
├── prompts/                   system prompt dùng cho AI
├── tests/test_app.py          11 test tự động
├── requirements.txt           thư viện để chạy app
├── requirements-dev.txt       thêm pytest để chạy test
├── .streamlit/secrets.toml.example   mẫu file key (không chứa key thật)
├── SETUP.md                   hướng dẫn này
├── README.md                  mô tả prototype và guardrail
├── test-log.md                nhật ký thử với người dùng
└── CHANGELOG.md               nhật ký thay đổi
```
