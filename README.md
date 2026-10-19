# Báo cáo bài tập 1 tuần: Đặt lịch tái khám hộ người thân với đúng bác sĩ cũ

Vinmec Exploration Sprint

| Thông tin | |
|---|---|
| Chương trình | Vinmec Exploration Sprint · Bài tập 1 tuần (K1–K3) |
| Khoảnh khắc nghiên cứu | Đặt lịch tái khám, nhìn từ phía người nhà đặt lịch hộ cha mẹ, ông bà |
| Thời gian thực hiện | 15–19/10/2026 |
| Dữ liệu | 3 phỏng vấn ẩn danh; kiểm thử ứng dụng MyVinmec và chatbot MIA; 6 nguồn tài liệu quốc tế |
| Sản phẩm | Journey map, need statement, 3 best practice, prototype có AI, đánh giá rủi ro, kế hoạch coach, `slides.pdf` (kèm bản trình chiếu `slides/slides.html`) |
| Sử dụng AI | Có, xem mục 3 "Phần do AI tạo" |
| Thuật ngữ | Xem [`THUAT-NGU.md`](THUAT-NGU.md) |

---

## Tóm tắt

**Bối cảnh.** Bài tập tìm hiểu một khoảnh khắc trong hành trình khám bệnh. Ban đầu tôi chọn khoảnh khắc đặt lịch khám, sau phỏng vấn thì thu hẹp lại thành đặt lịch tái khám.

**Phát hiện.**
- Cả 3 lần đặt lịch gần nhất của người tham gia đều do người nhà đặt hộ.
- Giả thuyết ban đầu "người bệnh khó chọn đúng chuyên khoa" không đúng, cả 3 người đều tự chấm mức chắc chắn 4/5.
- Điểm khó chịu nhất là **không đặt lại được đúng bác sĩ cũ khi tái khám**. P1 chấm khâu này 5/5 khó chịu. P2 không biết bác sĩ nào còn lịch gần nên chọn đại.
- Khi thử MyVinmec, tôi thấy app chỉ cho xem lịch trống theo từng ngày. MIA (chatbot AI trong MyVinmec) cũng không trả lời được về lịch trống.

**Need statement.**

> Cách để **giảm thời gian và số lần thao tác cần thiết để đặt lịch tái khám với đúng bác sĩ đang theo dõi người bệnh**, cho **người nhà đặt lịch hộ người thân** (cha mẹ, ông bà), trong bối cảnh **không biết bác sĩ đó còn trống lịch vào ngày nào, phải dò từng ngày hoặc chấp nhận một bác sĩ khác**.

**Hướng giải quyết.** Ba thực hành quốc tế cùng gợi ý một hướng: bác sĩ tạo sẵn phiếu tái khám (Epic Scheduling Tickets), hệ thống chủ động đưa ra lịch trống của đúng bác sĩ (Epic Fast Pass), và người nhà được đặt hộ khi người bệnh đồng ý (NHS App, ứng dụng của hệ thống y tế công Anh). Prototype mô phỏng hướng này, với các guardrail (cơ chế chặn rủi ro) rút từ lỗi đã thấy ở MIA: chậm hướng dẫn khẩn cấp, đưa ra chẩn đoán, không phát hiện thông tin sai.

**Giới hạn chính.**
- Cỡ mẫu nhỏ (n=3).
- Chưa có số liệu nền định lượng.
- Prototype chưa kịp thử với người dùng thật trong thời hạn bài tập. Kịch bản thử đã có trong `05-prototype/test-log.md`.

## 1. Mục lục

| Thư mục | Nội dung | File chính |
|---|---|---|
| [`01-phong-van/`](01-phong-van/) | Ghi chép dùng thử MyVinmec và MIA, interview guide, 3 cuộc phỏng vấn ẩn danh, tổng hợp insight, phân tích điểm đau | [`insight.md`](01-phong-van/insight.md), [`myvinmec-trial.md`](01-phong-van/myvinmec-trial.md), [`interview-guide.md`](01-phong-van/interview-guide.md), [`phong-van/P1.md`](01-phong-van/phong-van/P1.md) · [`P2`](01-phong-van/phong-van/P2.md) · [`P3`](01-phong-van/phong-van/P3.md), [`phan-tich-insight.md`](01-phong-van/phan-tich-insight.md), [`screenshots/`](01-phong-van/screenshots/) |
| [`02-journey-map/`](02-journey-map/) | Journey map có cảm xúc từng bước, workflow điểm đau chính | [`journey-map.md`](02-journey-map/journey-map.md), [`journey-map.png`](02-journey-map/journey-map.png), [`pain-workflow.png`](02-journey-map/pain-workflow.png) |
| [`03-need-statement/`](03-need-statement/) | Need statement theo mẫu Biodesign và bằng chứng | [`need-statement.md`](03-need-statement/need-statement.md) |
| [`04-best-practice/`](04-best-practice/) | 3 best practice quốc tế, nguồn, bài học cho Vinmec | [`best-practice.md`](04-best-practice/best-practice.md) |
| [`05-prototype/`](05-prototype/) | Prototype Streamlit có AI, mã nguồn, prompt, test tự động, kịch bản thử với người dùng (chưa kịp thực hiện) | [`README.md`](05-prototype/README.md), [`SETUP.md`](05-prototype/SETUP.md), [`app.py`](05-prototype/app.py), [`prompts/`](05-prototype/prompts/), [`test-log.md`](05-prototype/test-log.md), [`CHANGELOG.md`](05-prototype/CHANGELOG.md) |
| [`06-rui-ro-dao-duc/`](06-rui-ro-dao-duc/) | Rủi ro an toàn, đạo đức, cách giảm thiểu, đường chuyển tuyến khẩn cấp | [`rui-ro-dao-duc.md`](06-rui-ro-dao-duc/rui-ro-dao-duc.md) |
| [`07-coach-plan/`](07-coach-plan/) | Kế hoạch một trang: coach nhóm K4 theo khung Scrum (coach là Scrum Master, sprint bám các cổng của chương trình, Definition of Done) | [`coach-plan.md`](07-coach-plan/coach-plan.md), bản in A4 một trang [`coach-plan.pdf`](07-coach-plan/coach-plan.pdf) |
| [`slides.pdf`](slides.pdf) | Bản nộp chính: 10 slide tóm tắt để present | [`slides.pdf`](slides.pdf) |
| [`slides/`](slides/) | Bản trình chiếu HTML và mã nguồn slide. Cả hai bản xuất từ cùng một file Marp nên nội dung khớp nhau | [`slides.html`](slides/slides.html), [`slides.md`](slides/slides.md) |
| [`THUAT-NGU.md`](THUAT-NGU.md) | Thuật ngữ và từ viết tắt dùng trong repo | [`THUAT-NGU.md`](THUAT-NGU.md) |

**Slide**

- `slides.pdf` là bản nộp theo yêu cầu của đề, xem được trực tiếp trên GitHub.
- `slides/slides.html` dùng để trình chiếu trên trình duyệt. Cần mở từ thư mục repo đã clone về máy, vì ảnh trong slide dùng đường dẫn tương đối. Chuyển slide bằng phím mũi tên, bấm `F` để vào toàn màn hình. Bản này có speaker notes (ghi chú cho người trình bày, kèm thời lượng từng slide): bấm `P` để mở cửa sổ người trình bày. Bản PDF không hiển thị notes.
- Xuất lại cả hai bản sau khi sửa `slides/slides.md`:

```bash
docker run --rm -v "$PWD":/home/marp/app marpteam/marp-cli:v4.0.3 slides/slides.md --pdf  --allow-local-files -o slides.pdf
docker run --rm -v "$PWD":/home/marp/app marpteam/marp-cli:v4.0.3 slides/slides.md --html --allow-local-files -o slides/slides.html
```

Cách cài đặt và chạy prototype: [`05-prototype/SETUP.md`](05-prototype/SETUP.md). Không có API key (mã truy cập dịch vụ AI) thì app chạy ở chế độ không dùng AI.

## 2. Ràng buộc đạo đức đã tuân thủ

- Cả 3 người tham gia đồng ý phỏng vấn và ghi hình trước khi bắt đầu.
- Chỉ hỏi về trải nghiệm dịch vụ. Thông tin sức khỏe người tham gia tự kể được thay bằng `[đã ẩn]`.
- Người tham gia được ẩn danh thành P1–P3. Ghi chép gốc có tên thật và video phỏng vấn không đưa vào repo. Tên người thân trong ảnh chụp chatbot đã được che, thông tin EXIF (dữ liệu ẩn trong ảnh) đã được xóa.
- Không đưa lời khuyên y khoa. Kiểm thử MyVinmec dừng trước bước xác nhận, không tạo lịch thật. Câu hỏi khẩn cấp gửi MIA là tình huống giả định.
- Prototype chỉ dùng dữ liệu giả và tên bác sĩ hư cấu.

## 3. Phần do AI tạo

Đây là nơi khai báo duy nhất về việc dùng AI trong bài, theo yêu cầu "ghi rõ phần nội dung nào do AI tạo" của đề. Các file khác không lặp lại phần khai báo này. Riêng ghi chép P1–P3 có một dòng nói rõ nguồn gốc dữ liệu, và `05-prototype/prompts/` lưu các prompt đã dùng theo yêu cầu của đề.

Tôi dùng Claude (Claude Code) làm trợ lý trong suốt bài tập.

| Sản phẩm | AI thực hiện | Tôi thực hiện và quyết định |
|---|---|---|
| Interview guide | Gợi ý khung câu hỏi | Chỉnh sửa, chốt câu hỏi, xin đồng ý và phỏng vấn |
| Ghi chép P1–P3 | Chuẩn hóa định dạng, không đổi nội dung câu trả lời | Ghi chép trong và sau buổi phỏng vấn |
| Kiểm thử MyVinmec và MIA | Soạn kịch bản thử. Viết cột "Đánh giá" và phần "Nhận định" từ ghi nhận và ảnh chụp | Thử trên app, chụp ảnh, ghi cột "Kết quả" |
| Insight, phân tích điểm đau | Soạn bản tổng hợp từ ghi chép | Duyệt, chọn điểm đau chính (D1) |
| Journey map | Dựng sơ đồ Mermaid và bảng chi tiết | Duyệt các bước và điểm cảm xúc |
| Need statement | Soạn câu chữ và bố cục báo cáo | Chọn điểm đau trọng tâm, nhóm người dùng, loại các phương án khác, chốt câu need statement |
| Best practice | Tìm kiếm, đọc nguồn, tóm tắt số liệu | Chọn bài học cho Vinmec |
| Prototype | Viết mã nguồn, dữ liệu giả, test (xem [`05-prototype/prompts/README.md`](05-prototype/prompts/README.md)) | Đặt yêu cầu và guardrail, chạy thử (chưa kịp thử với người dùng thật) |
| Rủi ro và đạo đức | Soạn bản nháp từ kết quả kiểm thử | Đối chiếu với kết quả kiểm thử |
| Coach plan | Soạn bản nháp theo khung Scrum | Chốt lịch, vai trò và các tình huống kẹt từ kinh nghiệm làm bài |
| Slide, README, thuật ngữ | Soạn bản nháp, biên tập văn phong | Duyệt nội dung |

## 4. Giới hạn

- Mẫu nhỏ: 3 người, mỗi buổi 13–18 phút, đều là người quen, đều đặt hộ người thân. Chưa ai dùng MyVinmec.
- Chưa đo định lượng số lần thử để tìm lịch trống trên MyVinmec, mới có kết quả định tính.
- Trích dẫn lấy từ ghi chép, chưa đối chiếu nguyên văn với video.
- Thử MyVinmec bằng tài khoản mới, không có lịch sử khám, nên các tính năng sau khám (nhắc tái khám, kết quả) chỉ kiểm chứng được qua mô tả.
