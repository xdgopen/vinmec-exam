# Prototype: Đặt lịch tái khám hộ người thân

Streamlit (thư viện Python làm giao diện web), dữ liệu giả, có AI

| Thông tin tài liệu | |
|---|---|
| Dự án | Vinmec Exploration Sprint · Bài tập 1 tuần |
| Need statement | `../03-need-statement/need-statement.md` |
| Phiên bản · Ngày | 0.2.0 · 20/10/2026 (xem `CHANGELOG.md`) |
| Lưu ý | Prototype học tập, dữ liệu giả, không phải sản phẩm của Vinmec, không tư vấn y khoa |
| Thuật ngữ | Xem `../THUAT-NGU.md` |

---

> Hướng dẫn cài đặt và chạy từng bước (Python hoặc Docker), kèm cách xử lý lỗi thường gặp: [`SETUP.md`](SETUP.md).

## Tóm tắt

Người nhà có lịch tái khám với **đúng bác sĩ cũ** mà không phải dò từng ngày. App hiện toàn bộ lịch trống của bác sĩ đó quanh ngày hẹn. Có ba cách bắt đầu:

1. **Phiếu tái khám** do bác sĩ tạo (mô phỏng tính năng Vinmec chưa có).
2. **Giấy hẹn tái khám**: người nhà dán nội dung giấy hẹn in hoặc chép tay, app đọc và tạo phiếu.
3. **Gõ yêu cầu tự do**, ví dụ "bác sĩ An, giữa tháng 11".

**Bản hiện tại chạy hoàn toàn bằng luật (rule-based), chưa dùng AI thật.** Phần AI đã được thiết kế và nối sẵn trong code: prompt, khuôn dữ liệu, guardrail, điểm gọi AI. Phần này chỉ chạy khi có API key, và trong bài tập này **chưa được bật**. Mục "Rule-based và AI" bên dưới nói rõ luật đang làm gì, và AI được dự định dùng vào việc gì.

| Hạng mục | Trạng thái |
|---|---|
| Toàn bộ luồng chạy bằng luật | Đang chạy, 18 test tự động đạt |
| Phần AI (Claude Sonnet 5.5) | Đã thiết kế và nối sẵn trong code, **chưa bật, chưa chạy với AI thật**. Trong test, AI được giả lập để kiểm tra cách app gọi và dùng kết quả |
| Thử nghiệm với người dùng | Chưa kịp thực hiện trong thời hạn bài tập |

---

## Luồng

1. Người nhà chọn một trong ba cách: phiếu tái khám có sẵn, dán giấy hẹn, hoặc gõ yêu cầu.
2. **Kiểm tra khẩn cấp** bằng luật, chạy trước mọi bước. Có dấu hiệu nguy hiểm thì hiện nút Gọi 115 ngay và dừng.
3. **Giấy hẹn:** app bỏ các dòng có họ tên, năm sinh, chẩn đoán, đơn thuốc **trước khi đọc**. Luật đọc bác sĩ và ngày hẹn. Người nhà **kiểm tra và sửa** bác sĩ, ngày hẹn trước khi tạo phiếu.
4. **Yêu cầu tự do:** luật đọc người khám, bác sĩ, khoảng ngày, buổi.
5. **Tìm bác sĩ** không phân biệt dấu, khớp được tên gọi ngắn. Không chắc thì báo "không tìm thấy" và gợi ý, không tự đoán.
6. **Lịch trống** (mô phỏng Epic Fast Pass): hiện tất cả ngày còn trống quanh ngày hẹn. Kín lịch thì gợi ý giờ gần nhất và danh sách chờ.
7. **Xác nhận** (không tạo lịch thật): thông báo gửi cả người đặt và người khám, tự tạo nhắc lịch, đếm số thao tác.

## Rule-based và AI: luật đang làm gì, AI dùng vào việc gì

**Điểm đau** là người nhà phải tự nhớ lịch tái khám và tên bác sĩ, rồi dò lịch từng ngày (D1, D6 trong `../01-phong-van/phan-tich-insight.md`). Hiện bác sĩ chỉ dặn miệng hoặc đưa **giấy hẹn**. Vinmec chưa có phiếu tái khám điện tử.

### 1. Luật (rule-based) đang xử lý những gì

| Việc | Luật làm thế nào | Kết quả đã kiểm chứng |
|---|---|---|
| Kiểm tra khẩn cấp | Danh sách từ khóa tiếng Việt (có dấu và không dấu) và tiếng Anh, chạy trước mọi bước | Câu "bố tôi đột nhiên đau ngực, khó thở" chuyển ngay sang màn hình 115. Báo nhầm với câu phủ định ("tôi không bị đau ngực") |
| Bỏ thông tin trên giấy hẹn | Xóa dòng chứa họ tên, năm sinh, chẩn đoán, đơn thuốc, BHYT, địa chỉ… | GH-1 bỏ 3 dòng, GH-2 bỏ 2 dòng, tên bác sĩ và ngày hẹn vẫn còn |
| Đọc giấy hẹn | Tìm tên bác sĩ sau "Bác sĩ/BS", bỏ học hàm (ThS, BSCKII…). Đọc ngày dạng 12/11/2026. Hiểu "tái khám sau N ngày/tuần/tháng" tính từ ngày khám | GH-1 (bản in): Trần Minh An, ngày 12/11. GH-2 (chép tay, "sau 1 tháng"): Lê Thu Hà, ngày 20/11. **GH-3 (viết tắt, "đầu tháng 12"): không đọc được ngày**, người nhà tự chọn ở màn hình kiểm tra |
| Đọc yêu cầu gõ tự do | Danh sách người khám (bố, mẹ, ông, bà…), tên sau "bác sĩ", tên 4 khoa, ngày dạng 12/11, "đầu/giữa/cuối tháng N", "tuần sau", "tháng sau", "N tháng nữa", "sáng/chiều" | Câu theo các mẫu trên đọc đúng. Câu ngoài mẫu (ví dụ "sau đợt điều trị", "sau Tết") không đọc được ngày, app tự lấy 30 ngày tới |
| Tìm bác sĩ | Khớp theo từ, không phân biệt dấu, có so gần đúng để bắt lỗi chính tả | "bác sĩ An", "tran minh an" ra đúng bác sĩ. Tên không có thật thì báo "không tìm thấy". Trùng tên gọi thì hỏi người dùng |
| Hiện lịch trống, danh sách chờ | Lọc dữ liệu lịch theo bác sĩ, khoảng ngày, buổi | Hiện mọi ngày trống cùng lúc. Đây là phần giải quyết điểm đau "dò từng ngày" |

**Giới hạn của luật:** luật chỉ đọc được những mẫu đã viết sẵn. Giấy hẹn và cách người nhà nói về thời gian tái khám rất đa dạng (viết tắt, chép tay, "đầu năm sau", "sau Tết", "khi nào hết thuốc"). Mỗi kiểu mới lại cần thêm luật.

### 2. AI được dùng vào mục đích gì (thiết kế, chưa bật)

**Mục đích chính: đọc những giấy hẹn mà luật không đọc được, để tạo phiếu tái khám.** Có phiếu thì người nhà không phải nhớ ngày hẹn (D6) và tên bác sĩ (D1), và **Vinmec không cần làm tính năng mới**, vì giấy hẹn vốn đã có. Ví dụ với GH-3, "Gặp lại BS Nam bên tim mạch vào đầu tháng 12": luật không hiểu ngày, AI được thiết kế để đọc ra ngày hẹn đầu tháng 12.

**Mục đích phụ: đọc yêu cầu gõ tự do mà luật không hiểu**, ví dụ "bố cần gặp lại bác sĩ An sau đợt điều trị".

**AI được đặt ở đâu trong luồng (đã có sẵn trong code):**

```
Giấy hẹn / câu gõ
  → Bỏ dòng định danh, sức khỏe (luật)
  → Kiểm tra khẩn cấp (luật)
  → Luật đọc bác sĩ, ngày hẹn
       ├─ Đủ thông tin → dùng luôn, KHÔNG gọi AI
       └─ Chưa đủ → [khi có API key] AI đọc phần văn bản đã bỏ thông tin
                     → [không có key, như hiện tại] người nhà tự bổ sung
  → Người nhà kiểm tra, sửa → tìm bác sĩ, hiện lịch trống (luật)
```

**Đã chuẩn bị sẵn cho AI:**
- System prompt: `prompts/slip-system-prompt.md` (giấy hẹn) và `prompts/extract-system-prompt.md` (câu gõ).
- Khuôn JSON bắt buộc cho đầu ra, và bước kiểm tra lại kết quả.
- Guardrail: AI chỉ nhận văn bản đã bỏ thông tin. AI không chẩn đoán, không tạo lịch hay tên bác sĩ. Kết quả phải qua bước người nhà kiểm tra.
- Test giả lập AI: câu đủ thông tin thì không gọi AI, câu thiếu thì gọi, và AI chỉ nhận văn bản đã bỏ thông tin.

**Vì sao chọn "luật trước, AI sau":**
- Phần lớn giấy hẹn theo mẫu quen thuộc được xử lý tại chỗ, không gửi dữ liệu ra dịch vụ AI.
- Không tốn phí và giải thích được kết quả.
- AI chỉ được dùng cho đúng phần luật không làm được.

**Hướng phát triển AI tiếp theo (ý tưởng, chưa làm):**
- Đọc trực tiếp **ảnh chụp** giấy hẹn, thay vì dán văn bản.
- Soạn tin nhắc tái khám dễ hiểu gửi cho người lớn tuổi và người nhà.
- Cả hai vẫn giữ nguyên tắc: AI không chẩn đoán, người dùng xác nhận kết quả.

**Việc cần làm trước khi bật AI thật:**
- Chạy thử với API key trên các giấy hẹn mẫu, nhất là GH-3.
- Đo tỷ lệ đọc đúng so với luật.
- Đánh giá việc gửi dữ liệu ra dịch vụ AI theo quy định bảo vệ dữ liệu cá nhân.

## Chạy app

Xem [`SETUP.md`](SETUP.md): chạy bằng Python (`streamlit run app.py`) hoặc Docker (`docker compose up --build`). Bản hiện tại chạy bằng luật, không cần API key. Những câu và giấy hẹn mà luật không đọc được thì người dùng tự bổ sung ở màn hình kiểm tra.

## Test

```bash
python -m pytest tests -q     # 18 test; phần AI được giả lập, không cần key
```

Test kiểm tra:
- Luồng phiếu, lịch trống, danh sách chờ, khẩn cấp, bác sĩ không có thật, tên gọi ngắn, trùng tên.
- **Bản 0.2:**
  - Luật đọc đúng "bà" (không nhầm "ba"), không coi "dặn" là tên bác sĩ, hiểu "tuần sau", "tháng sau", "3 tháng nữa".
  - Câu đủ thông tin thì không gọi AI. Câu thiếu thông tin thì gọi AI.
  - Bỏ đúng các dòng định danh và sức khỏe trên giấy hẹn.
  - Đọc đúng giấy hẹn GH-1 và GH-2 bằng luật. GH-3 cần AI, và AI chỉ nhận văn bản đã bỏ thông tin.
  - Luồng giấy hẹn chạy trên giao diện. Giấy hẹn có dấu hiệu khẩn cấp thì chuyển sang màn hình 115.

## Guardrail (cơ chế chặn rủi ro)

| Rủi ro | Cách xử lý trong prototype | Bài học từ |
|---|---|---|
| Bỏ lỡ tình huống cấp cứu | Từ khóa tiếng Việt (có dấu và không dấu) và tiếng Anh, kiểm tra trước mọi bước, kể cả với giấy hẹn. Không hỏi thêm trước khi hiện 115 | MIA (chatbot của MyVinmec) M5: hỏi giới tính, tuổi trước khi hiện 115. M9: tiếng Anh không có 115 |
| AI chẩn đoán | Prompt cấm chẩn đoán. LLM (mô hình ngôn ngữ lớn) chỉ trích JSON theo schema (khuôn dữ liệu) | MIA M6 |
| AI bịa bác sĩ, bịa lịch, đọc sai ngày hẹn | Bác sĩ và lịch lấy từ dữ liệu. Không khớp chắc chắn thì báo "không tìm thấy". Người nhà kiểm tra, sửa bác sĩ và ngày hẹn trước khi tạo phiếu | MIA M2 |
| Giấy hẹn chứa thông tin y tế | Bỏ các dòng họ tên, năm sinh, chẩn đoán, đơn thuốc **trước khi đọc** (kể cả trước khi gửi cho AI). Chỉ dùng dữ liệu giả | MIA M1, M2 (lộ tên người thân) |
| Gửi dữ liệu ra ngoài không cần thiết | Luật trước, AI sau: đọc được bằng luật thì không gọi AI | — |
| AI lỗi hoặc không có key | Dùng kết quả của luật, nhãn "Chế độ không dùng AI", người nhà tự bổ sung | — |

**Giới hạn:**
- Danh sách từ khóa khẩn cấp và danh sách từ cần bỏ trên giấy hẹn chưa đầy đủ.
- Đây là lưới an toàn tối thiểu, không thay việc phân loại cấp cứu của nhân viên y tế hay quy trình bảo vệ dữ liệu thật.

## Ảnh chụp

Ảnh 01, 04, 05, 06 chụp từ bản 0.2.0. Ảnh 02, 03 chụp từ bản 0.1 (giao diện hai màn hình này không đổi). Tất cả chạy bằng luật, chưa bật AI.

| Ảnh | Nội dung |
|---|---|
| [`01-home.png`](screenshots/01-home.png) | Màn hình đầu: phiếu tái khám có sẵn, mục tạo phiếu từ giấy hẹn |
| [`04-giay-hen.png`](screenshots/04-giay-hen.png) | Dán giấy hẹn mẫu GH-2 (chép tay, "tái khám sau 1 tháng") |
| [`05-kiem-tra-phieu.png`](screenshots/05-kiem-tra-phieu.png) | Kiểm tra phiếu đọc từ giấy hẹn GH-1: đã bỏ 3 dòng thông tin, bác sĩ Trần Minh An, ngày hẹn 12/11 |
| [`06-lich-trong-giay-hen.png`](screenshots/06-lich-trong-giay-hen.png) | Lịch trống quanh ngày hẹn 12/11: 8 ngày, 17 giờ khám |
| [`02-lich-trong.png`](screenshots/02-lich-trong.png) | Lịch trống khi mở phiếu tái khám PT-001 |
| [`03-khan-cap.png`](screenshots/03-khan-cap.png) | Câu có dấu hiệu khẩn cấp: dừng đặt lịch, hiện nút gọi 115 |

## Cấu trúc

```
app.py                 # giao diện Streamlit
core.py                # logic: khẩn cấp, đọc yêu cầu, đọc giấy hẹn, tìm bác sĩ, lịch trống
mock-data/             # doctors.json, slots.json, tickets.json, slips.json (giấy hẹn mẫu, giả)
prompts/               # system prompt cho AI: đọc yêu cầu, đọc giấy hẹn
tests/test_app.py      # 18 test không giao diện
screenshots/           # ảnh chụp app
test-log.md            # kịch bản thử với 2–3 người (chưa kịp thực hiện)
CHANGELOG.md           # nhật ký thay đổi
SETUP.md               # hướng dẫn cài đặt và chạy
requirements.txt       # thư viện để chạy app
requirements-dev.txt   # thêm pytest để chạy test
Dockerfile             # đóng gói thành image Docker
docker-compose.yml     # chạy bằng: docker compose up --build
```
