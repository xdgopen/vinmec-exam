# Nhật ký thay đổi (changelog)

## v0.2.0 – 20/10/2026 (đọc giấy hẹn, chưa kịp thử với người dùng thật)

- **Trạng thái AI:** app chạy bằng luật. Phần AI đọc giấy hẹn và câu gõ đã được thiết kế và nối sẵn (prompt, khuôn JSON, guardrail, test giả lập) nhưng **chưa bật**, chưa chạy với AI thật.
- **Luồng mới "Tạo phiếu từ giấy hẹn":** người nhà dán nội dung giấy hẹn tái khám (in hoặc chép tay, dữ liệu giả, 3 mẫu GH-1 đến GH-3). App đọc bác sĩ và ngày hẹn rồi tạo phiếu, không cần bệnh viện có phiếu điện tử. Màn hình "Kiểm tra phiếu tái khám" cho người nhà xem và sửa bác sĩ, ngày hẹn, người khám trước khi tìm lịch. App tìm lịch từ 7 ngày trước đến 7 ngày sau ngày hẹn.
- **Bỏ thông tin trước khi đọc:** các dòng có họ tên, năm sinh, chẩn đoán, đơn thuốc, BHYT… bị bỏ trước khi luật hoặc AI đọc giấy hẹn. Kiểm tra khẩn cấp vẫn chạy trên phần còn lại.
- **Luật trước, AI sau** cho cả giấy hẹn và yêu cầu tự do. Luật đọc đủ bác sĩ và ngày thì không gọi AI. Nhãn chế độ hiện rõ đang dùng luật, AI, hay "không dùng AI".
- **Sửa bộ đọc theo luật:** "bà" không còn bị đọc thành "ba". "Bác sĩ dặn…" không còn coi "dặn" là tên bác sĩ. Hiểu thêm "tuần sau", "tháng sau", "N tháng nữa", "sau N tuần".
- Thêm `prompts/slip-system-prompt.md`, `mock-data/slips.json`, 7 test (tổng 18, AI được giả lập trong test).

## v0.1.2 – 20/10/2026 (đóng gói Docker, chưa kịp thử với người dùng thật)

- Thêm `Dockerfile` (image `python:3.13-slim`, chạy bằng user thường, có healthcheck), `docker-compose.yml` và `.dockerignore`. API key chỉ truyền lúc chạy qua biến môi trường, không nằm trong image. Mã nguồn app không đổi.
- `SETUP.md` thêm mục 6 hướng dẫn chạy bằng Docker.

## v0.1.1 – 19/10/2026 (sửa lỗi phát hiện khi rà soát, chưa kịp thử với người dùng thật)

- Tìm bác sĩ theo tên ngắn. Trước đây gõ "bác sĩ An" thì báo không tìm thấy, không gợi ý, dù người nhà thường chỉ nhớ tên gọi. Nay khớp theo từ: mọi từ người dùng gõ phải có trong tên bác sĩ và phải có tên gọi (từ cuối). "An", "Minh An", "Tran Minh An" đều ra đúng bác sĩ. "Anh" không bị nhầm thành "An". Gõ mỗi tên đệm ("Minh") thì không đoán.
- Trùng tên gọi: app hiện "Có N bác sĩ tên …, hãy chọn bác sĩ đã khám lần trước" và liệt kê để chọn, không tự chọn. Nếu câu yêu cầu có nêu khoa thì dùng khoa để lọc.
- Thêm 4 test (tổng 11), tất cả qua.
- Thêm `SETUP.md` (hướng dẫn cài đặt, chạy, bật AI, deploy, xử lý lỗi) và `requirements-dev.txt` (thêm pytest, trước đây thiếu nên không chạy được test sau khi cài). Đã cài thử từ đầu bằng pip trên Python 3.14: 11 test qua, app khởi động bình thường.

## v0.1 – 19/10/2026 (bản đầu, chưa kịp thử với người dùng thật)

- Màn hình "Phiếu tái khám" (mô phỏng BP1): 3 phiếu giả, mỗi phiếu gắn sẵn bác sĩ và khoảng thời gian.
- Ô nhập yêu cầu tự do. AI (`claude-sonnet-5-5`) trích JSON (dữ liệu có cấu trúc) theo schema. Không có key hoặc AI lỗi thì dùng luật.
- Kiểm tra dấu hiệu khẩn cấp theo luật, chạy trước mọi bước, hiện nút gọi 115 ngay, không hỏi thêm (bài học MIA M5, M9; MIA là chatbot của MyVinmec).
- Tìm bác sĩ không phân biệt dấu. Không chắc thì nói "không tìm thấy" và gợi ý, không tự đoán (bài học MIA M2).
- Màn hình lịch trống (mô phỏng BP2): hiện tất cả ngày còn trống trong khoảng, không bắt dò từng ngày. Kín lịch thì gợi ý 3 giờ gần nhất và danh sách chờ, thông báo gửi cả người đặt và người khám.
- Màn hình xác nhận (không tạo lịch thật), đếm thao tác.
- 7 test không giao diện (`tests/test_app.py`), tất cả qua.

## Sau khi thử với người dùng

*(Ghi các thay đổi theo test-log.md: v0.2, v0.3…)*
