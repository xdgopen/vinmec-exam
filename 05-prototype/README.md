# Prototype: Đặt lịch tái khám hộ người thân

Streamlit (thư viện Python làm giao diện web), dữ liệu giả, có AI

| Thông tin tài liệu | |
|---|---|
| Dự án | Vinmec Exploration Sprint · Bài tập 1 tuần |
| Need statement | `../03-need-statement/need-statement.md` |
| Phiên bản · Ngày | 0.1.1 · 19/10/2026 (xem `CHANGELOG.md`) |
| Lưu ý | Prototype học tập, dữ liệu giả, không phải sản phẩm của Vinmec, không tư vấn y khoa |
| Thuật ngữ | Xem `../THUAT-NGU.md` |

---

> Hướng dẫn cài đặt và chạy từng bước, gồm cả Windows và cách xử lý lỗi thường gặp: [`SETUP.md`](SETUP.md).

## Tóm tắt

Luồng đặt lịch bắt đầu từ phiếu tái khám do bác sĩ tạo. App hiện **toàn bộ lịch trống của đúng bác sĩ** trong khoảng tái khám, không phải dò từng ngày.

- AI: Claude chỉ trích xuất thông tin lịch hẹn từ câu gõ tự do. Bác sĩ và lịch trống lấy từ dữ liệu.
- An toàn: luật kiểm tra dấu hiệu khẩn cấp chạy trước mọi bước, hiện hướng dẫn gọi 115 ngay.
- Hiện trạng:

| Hạng mục | Trạng thái |
|---|---|
| 11 test tự động (chế độ không dùng AI) | Đạt |
| Luồng gọi AI thật | Chưa kiểm chứng |
| Thử nghiệm với người dùng | Chưa kịp thực hiện trong thời hạn bài tập |

---

## Luồng

1. Phiếu tái khám (mô phỏng BP1, Epic Scheduling Tickets) gắn sẵn bác sĩ và khoảng thời gian. Hoặc gõ yêu cầu tự do.
2. Kiểm tra khẩn cấp bằng luật, chạy trước mọi bước. Có dấu hiệu nguy hiểm thì hiện nút **Gọi 115** ngay và dừng.
3. AI trích yêu cầu tự do thành JSON (dữ liệu có cấu trúc): người khám, bác sĩ, khoảng ngày, buổi. Không có key thì dùng bộ đọc theo luật.
4. Tìm bác sĩ, không phân biệt dấu. Không chắc thì báo "không tìm thấy" và gợi ý, không tự đoán.
5. Lịch trống (mô phỏng BP2, Epic Fast Pass): hiện tất cả ngày còn trống trong khoảng. Kín lịch thì gợi ý giờ gần nhất và danh sách chờ.
6. Xác nhận (không tạo lịch thật): thông báo gửi cả người đặt và người khám, tự tạo nhắc lịch, đếm số thao tác.

## Chạy local

```bash
cd 05-prototype
uv venv && source .venv/bin/activate      # hoặc: python -m venv .venv
uv pip install -r requirements.txt        # hoặc: pip install -r requirements.txt
streamlit run app.py
```

Không có API key (mã truy cập Claude) app vẫn chạy, ở chế độ không dùng AI. Để bật AI:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # điền ANTHROPIC_API_KEY
# hoặc: export ANTHROPIC_API_KEY=...
```

`.streamlit/secrets.toml` đã nằm trong `.gitignore`. Không commit key lên repo.

## Deploy lên Streamlit Community Cloud

1. Đẩy repo lên GitHub.
2. Trên share.streamlit.io, chọn New app, chọn repo và main file `05-prototype/app.py`.
3. Vào Settings, mục Secrets, dán `ANTHROPIC_API_KEY = "..."`.

## Test

```bash
python -m pytest tests -q     # 11 test, chạy đường không dùng AI
```

Test kiểm tra: luồng phiếu hiện nhiều ngày trống và xác nhận được. Phiếu kín lịch hiện giờ gần nhất và danh sách chờ. Câu khẩn cấp hiện 115, không cho đặt. Bác sĩ không có thật báo "không tìm thấy". Yêu cầu tự do và tên gọi ngắn ("bác sĩ An") vào được lịch trống. Trùng tên gọi thì hỏi người dùng chọn.

## Guardrail (cơ chế chặn rủi ro)

| Rủi ro | Cách xử lý trong prototype | Bài học từ |
|---|---|---|
| Bỏ lỡ tình huống cấp cứu | Từ khóa tiếng Việt (có dấu và không dấu) và tiếng Anh, kiểm tra trước mọi bước, không hỏi thêm trước khi hiện 115 | MIA (chatbot của MyVinmec) M5: hỏi giới tính, tuổi trước khi hiện 115. M9: tiếng Anh không có 115 |
| AI chẩn đoán | Prompt cấm chẩn đoán. LLM (mô hình ngôn ngữ lớn) chỉ trích JSON theo schema (khuôn dữ liệu) | MIA M6 |
| AI bịa bác sĩ, bịa lịch | Bác sĩ và lịch lấy từ dữ liệu, không từ LLM; không khớp chắc chắn thì báo "không tìm thấy" | MIA M2 |
| AI lỗi hoặc không có key | Bộ đọc theo luật làm phương án dự phòng (fallback), có nhãn "Chế độ không dùng AI" | — |
| Dữ liệu cá nhân | Toàn bộ dữ liệu giả, tên bác sĩ hư cấu; không hỏi triệu chứng | MIA M1, M2 (lộ tên người thân); IMG_4760 (bắt buộc mô tả triệu chứng) |

**Giới hạn:** danh sách từ khóa khẩn cấp chưa đầy đủ, có thể báo nhầm. Đây là lưới an toàn tối thiểu, không thay việc phân loại cấp cứu của nhân viên y tế.

## Cấu trúc

```
app.py                 # giao diện Streamlit
core.py                # logic: khẩn cấp, trích xuất, tìm bác sĩ, lịch trống
mock-data/             # doctors.json, slots.json, tickets.json (giả)
prompts/               # prompt đã dùng
tests/test_app.py      # test không giao diện
screenshots/           # ảnh chụp app (lịch trống, khẩn cấp)
test-log.md            # kịch bản thử với 2–3 người (chưa kịp thực hiện)
CHANGELOG.md           # nhật ký thay đổi
SETUP.md               # hướng dẫn cài đặt và chạy
requirements.txt       # thư viện để chạy app
requirements-dev.txt   # thêm pytest để chạy test
```
