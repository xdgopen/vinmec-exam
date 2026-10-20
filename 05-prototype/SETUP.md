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

**Thử tay 6 tình huống (cả hai cách)**

| # | Thao tác | Kết quả đúng |
|---|---|---|
| 1 | Ở phiếu tái khám PT-001, bấm "Xem lịch trống và đặt" | Hiện nhiều ngày trống của bác sĩ Trần Minh An cùng lúc. Chọn một giờ thì sang màn hình xác nhận |
| 2 | Gõ `đặt tái khám cho mẹ với bác sĩ An giữa tháng 11` rồi bấm "Tìm lịch" | Tìm được bác sĩ Trần Minh An khi chỉ gõ tên gọi |
| 3 | Gõ `đặt tái khám cho bố với bác sĩ Nguyễn Thanh David` | Báo "Không tìm thấy" và không tự đoán bác sĩ |
| 4 | Gõ `bố tôi đột nhiên đau ngực, khó thở` | Hiện ngay khung cấp cứu và nút "Gọi 115". Không cho đặt lịch |
| 5 | Ở mục "Tạo phiếu từ giấy hẹn", bấm "Mẫu GH-2" rồi "Tạo phiếu tái khám" | Màn hình kiểm tra hiện bác sĩ Lê Thu Hà, ngày hẹn 20/11/2026, báo đã bỏ 2 dòng thông tin cá nhân. Bấm "Đúng, tạo phiếu…" thì sang lịch trống |
| 6 | Bấm "Mẫu GH-3" rồi "Tạo phiếu tái khám" (không có API key) | Nhãn "Chế độ không dùng AI", báo chưa đọc được ngày hẹn và cho người dùng tự chọn. Có key thì AI đọc được ngày hẹn |

## 6. Hướng dẫn sử dụng từng bước

Mở app tại `http://localhost:8501`. Màn hình đầu có ba cách bắt đầu, xếp từ trên xuống: **Phiếu tái khám bác sĩ đã hẹn**, **Tạo phiếu từ giấy hẹn**, **Hoặc nhập yêu cầu**. Toàn bộ dữ liệu là dữ liệu giả, và không có lịch thật nào được tạo.

Bản hiện tại chạy bằng luật, chưa bật AI. Nhãn nhỏ phía trên mỗi màn hình cho biết thông tin được đọc bằng cách nào. "Đọc bằng luật" nghĩa là luật đã đọc đủ. "Chế độ không dùng AI" nghĩa là luật chưa đọc đủ và bạn cần tự bổ sung.

### Cách 1: đặt lịch từ phiếu tái khám có sẵn

1. Ở mục **Phiếu tái khám bác sĩ đã hẹn**, xem 3 phiếu mẫu. Mỗi phiếu ghi người khám, bác sĩ và khoảng thời gian tái khám.
2. Ở phiếu đầu tiên (Bố, ThS.BS Trần Minh An), bấm **Xem lịch trống và đặt**.
3. Màn hình **Lịch trống của bác sĩ** hiện tất cả các ngày bác sĩ còn trống trong khoảng tái khám, mỗi ngày kèm các giờ còn trống. Bấm một giờ, ví dụ `08:30`.
4. Màn hình **Xác nhận lịch tái khám** hiện người khám, bác sĩ, thời gian, người nhận thông báo và lịch nhắc. Bấm **Xác nhận (mô phỏng)**.
5. App báo đã đặt (mô phỏng) và hiện **số thao tác** từ đầu đến khi có lịch. Bấm **Đặt lịch khác** để quay về màn hình đầu.

**Khi bác sĩ đã kín lịch:** mở phiếu thứ hai (Mẹ, TS.BS Lê Thu Hà). App báo bác sĩ đã kín lịch trong khoảng này và gợi ý 3 giờ trống gần nhất sau đó. Bấm **🔔 Báo cho tôi khi có lịch sớm hơn** để vào danh sách chờ (mô phỏng). Thông báo sẽ gửi cho cả người đặt và người khám.

### Cách 2: tạo phiếu từ giấy hẹn

1. Ở mục **Chưa có phiếu? Tạo phiếu từ giấy hẹn**, bấm **Mẫu GH-1** để điền sẵn một giấy hẹn mẫu. Bạn cũng có thể tự dán nội dung giấy hẹn (dữ liệu giả) vào ô **Nội dung giấy hẹn**.
2. Bấm **Tạo phiếu tái khám**.
3. Màn hình **Kiểm tra phiếu tái khám** hiện:
   - số dòng có thông tin cá nhân hoặc sức khỏe đã bị bỏ trước khi đọc (GH-1 bỏ 3 dòng);
   - bác sĩ đọc được (Trần Minh An) và ngày hẹn đọc được (12/11/2026);
   - khoảng app sẽ tìm lịch: từ 7 ngày trước đến 7 ngày sau ngày hẹn.
4. Kiểm tra lại, sửa nếu cần: chọn **Bác sĩ đã khám**, chỉnh **Ngày hẹn tái khám**, chọn **Người khám**.
5. Bấm **Đúng, tạo phiếu và xem lịch trống**. App hiện mọi ngày trống quanh ngày hẹn. Từ đây, chọn giờ và xác nhận giống bước 3–5 của cách 1.

Ba giấy hẹn mẫu cho kết quả khác nhau:

| Mẫu | Đặc điểm | Kết quả |
|---|---|---|
| GH-1 | Bản in, có ngày hẹn cụ thể | Luật đọc đủ bác sĩ và ngày hẹn 12/11 |
| GH-2 | Chép tay, chỉ ghi "tái khám sau 1 tháng" | Luật tính ngày hẹn 20/11 từ ngày khám. Bác sĩ Lê Thu Hà đã kín lịch quanh ngày này, nên app gợi ý giờ gần nhất và danh sách chờ |
| GH-3 | Viết tắt, ghi "đầu tháng 12" | Luật đọc được bác sĩ nhưng **không đọc được ngày hẹn**, app hiện "Chế độ không dùng AI". Bạn tự chọn ngày ở màn hình kiểm tra. Đây là loại giấy AI được thiết kế để đọc khi bật |

### Cách 3: gõ yêu cầu tự do

1. Ở mục **Hoặc nhập yêu cầu**, gõ một câu, ví dụ: `đặt tái khám cho mẹ với bác sĩ An giữa tháng 11, buổi sáng`.
2. Bấm **Tìm lịch**. App đọc người khám, bác sĩ, khoảng ngày, buổi. Bạn chỉ cần gõ tên gọi ("An"), có dấu hay không đều được.
3. Nếu tìm được bác sĩ, app vào thẳng màn hình lịch trống. Chọn giờ và xác nhận như cách 1.
4. Nếu không tìm được bác sĩ (ví dụ gõ `bác sĩ Nguyễn Thanh David`), app báo **Không tìm thấy** và cho chọn từ danh sách, không tự đoán.

Một số cách nói về thời gian luật đọc được: `12/11` hoặc `từ 12/11 đến 20/11`, `đầu/giữa/cuối tháng 11`, `tuần sau`, `tháng sau`, `3 tháng nữa`. Nếu câu không có thời gian, app tìm lịch trong 30 ngày tới.

### Tình huống khẩn cấp

Ở ô giấy hẹn hoặc ô yêu cầu, gõ một câu có dấu hiệu nguy hiểm, ví dụ `bố tôi đột nhiên đau ngực, khó thở`, rồi bấm nút tương ứng. App **dừng luồng đặt lịch ngay**, hiện cảnh báo và nút **📞 Gọi 115**, không hỏi thêm thông tin. Bấm **Quay lại** để về màn hình đầu.

### Quay lại và làm lại

Mỗi màn hình đều có nút **Quay lại**. Nút này xóa thông tin đang nhập và đưa bạn về màn hình đầu.

## 7. Đưa lên mạng để có link (Streamlit Community Cloud)

1. Đẩy repo lên GitHub.
2. Vào share.streamlit.io, đăng nhập bằng GitHub, chọn **Create app**.
3. Chọn repo và nhánh. Ở mục *Main file path* điền `05-prototype/app.py`.
4. Nếu muốn bật AI: vào *Advanced settings*, phần *Secrets*, dán `ANTHROPIC_API_KEY = "sk-ant-..."`.
5. Bấm **Deploy**. Sau vài phút sẽ có link dạng `https://<tên-app>.streamlit.app`. Dán link này vào README.

## 8. Lỗi thường gặp

| Lỗi | Nguyên nhân | Cách xử lý |
|---|---|---|
| `streamlit: command not found` | Chưa kích hoạt môi trường ảo | Chạy lại `source .venv/bin/activate` (Windows: `.venv\Scripts\Activate.ps1`), hoặc dùng `python -m streamlit run app.py` |
| `ModuleNotFoundError: streamlit` hoặc `anthropic` | Chưa cài thư viện, hoặc cài vào Python khác | Kích hoạt môi trường ảo rồi chạy lại `pip install -r requirements-dev.txt` |
| `Port 8501 is already in use`, hoặc Docker báo `port is already allocated` | Cổng 8501 đang bị dùng | Cách A: `streamlit run app.py --server.port 8502`. Cách B: đổi cổng bên trái, ví dụ `-p 8502:8501` (hoặc `"8502:8501"` trong `docker-compose.yml`), rồi mở `http://localhost:8502` |
| `Cannot connect to the Docker daemon` | Docker Desktop chưa chạy | Mở Docker Desktop, đợi biểu tượng báo đang chạy rồi thử lại |
| Build Docker dừng ở `pip install` hoặc báo lỗi mạng | Mạng chậm hoặc bị chặn khi tải thư viện từ PyPI | Chạy lại lệnh build. Các gói đã tải xong sẽ không phải tải lại nếu bước đó đã hoàn tất |
| Đã điền key mà vẫn hiện "Chế độ không dùng AI" | Key sai, hết hạn mức, model không truy cập được, hoặc key chưa được đưa vào đúng chỗ | Kiểm tra lại theo bảng ở mục 4. Với Docker, key phải được truyền bằng `-e` hoặc biến môi trường trước khi chạy Compose |
| Trình duyệt không tự mở | Chạy trên máy chủ, chế độ headless hoặc Docker | Mở thủ công `http://localhost:8501` |

## 9. Cấu trúc thư mục

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
