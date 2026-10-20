# Prompt đã dùng

## 1. Prompt chạy trong prototype

| File | Dùng ở đâu | Ghi chú |
|---|---|---|
| `extract-system-prompt.md` | `core.extract_with_llm()`, system prompt (hướng dẫn cố định) của `claude-sonnet-5-5` | `{today}` thay bằng ngày hiện tại. Đầu ra ràng buộc bằng JSON schema (`output_config.format`), sau đó kiểm tra lại bằng `core.validate()`. Chỉ được gọi khi luật chưa đọc đủ bác sĩ và khoảng ngày |
| `slip-system-prompt.md` | `core.slip_with_llm()`, đọc giấy hẹn tái khám | Chỉ nhận văn bản đã bỏ các dòng định danh và sức khỏe (`core.redact`). Chỉ trích bác sĩ, khoa, ngày khám, ngày hẹn hoặc khoảng hẹn. Chỉ được gọi khi luật chưa đọc đủ |

Guardrail (cơ chế chặn rủi ro) nằm trong code, không trong prompt, vì không nên giao việc an toàn cho LLM (mô hình ngôn ngữ lớn):

- Kiểm tra dấu hiệu khẩn cấp bằng luật trước khi gọi LLM (`core.red_flag`).
- LLM chỉ trích xuất. Tìm bác sĩ và lịch trống do code làm trên dữ liệu giả, nên LLM không bịa được bác sĩ hay lịch.
- Tên bác sĩ không khớp chắc chắn thì báo "không tìm thấy" (`core.match_doctor`).

## 2. Prompt dùng để dựng prototype (do AI tạo)

Toàn bộ mã nguồn, dữ liệu giả, test và tài liệu trong `05-prototype/` do Claude Code (Claude Opus 5.5) viết theo yêu cầu của tôi ngày 19/10/2026. Yêu cầu chính:

> Xây prototype Streamlit cho luồng "người nhà đặt lịch tái khám hộ người thân với đúng bác sĩ cũ": màn hình phiếu tái khám (mô phỏng Epic Scheduling Tickets), kiểm tra dấu hiệu khẩn cấp bằng luật chạy trước mọi bước và hiện nút gọi 115, LLM trích JSON từ yêu cầu tự do (không chẩn đoán, không bịa bác sĩ), tìm bác sĩ không phân biệt dấu và báo "không tìm thấy" khi không chắc, hiện tất cả ngày còn trống trong khoảng (mô phỏng Fast Pass), danh sách chờ gửi thông báo cho cả người đặt và người khám, màn hình xác nhận không tạo lịch thật. Có test không giao diện và log thử để trống.

Bản v0.1.1 (19/10/2026) sửa thêm theo yêu cầu "sửa lỗi tìm bác sĩ theo tên ngắn trong prototype" (chi tiết trong `../CHANGELOG.md`).

Bản v0.2.0 (20/10/2026) làm theo yêu cầu "làm phương án B": thêm luồng AI đọc giấy hẹn tái khám để tạo phiếu, đảo thứ tự thành luật trước và AI sau, sửa lỗi của bộ đọc theo luật.

Kiểm chứng: 18 test không giao diện đạt (AI được giả lập trong test). Tôi đã chạy app và chụp màn hình (`../screenshots/`). Chưa chạy gọi Claude thật vì chưa có API key.
