# Nhật ký thử nghiệm prototype với người dùng

| Thông tin tài liệu | |
|---|---|
| Dự án | Vinmec Exploration Sprint · Bài tập 1 tuần |
| Yêu cầu | Thử với 2–3 người; ghi ai thử, làm gì, gặp gì, sửa gì sau đó |
| Người thử | Ẩn danh T1–T3. Không hỏi về tình trạng sức khỏe. Mọi tình huống là giả định |
| Phiên bản prototype | 0.2.0 |
| Thuật ngữ | Xem `../THUAT-NGU.md` |
| Trạng thái | **Chưa kịp thực hiện trong thời hạn bài tập (19/10/2026).** Bảng kết quả để trống, không điền khi chưa thử thật |

---

## Tóm tắt

Mỗi người thử làm cùng 3 nhiệm vụ:

1. Đặt lịch tái khám từ phiếu. Đo số thao tác và thời gian để so với MyVinmec.
2. Nhập tên bác sĩ sai chính tả hoặc không tồn tại.
3. Nhập câu có dấu hiệu khẩn cấp.

---

## 1. Kịch bản thử (giống nhau cho mọi người)

| Mã | Nhiệm vụ đưa cho người thử | Kỳ vọng |
|---|---|---|
| A | "Bác sĩ đã hẹn bố bạn tái khám. Hãy đặt lịch tái khám cho bố với đúng bác sĩ đó." (dùng phiếu PT-001) | Thấy ngay nhiều ngày trống, chọn giờ, xác nhận |
| B | "Gõ yêu cầu đặt lịch cho mẹ với bác sĩ *Le Thu Ha* (gõ không dấu) hoặc *bác sĩ Nguyễn Thanh David*." | Tên đúng nhưng không dấu thì vẫn tìm được; tên không có thật thì app nói rõ "không tìm thấy" và không tự đoán |
| C | "Gõ: bố tôi đột nhiên đau ngực, khó thở, nên đặt lịch không?" | App hiện nút gọi 115 ngay, không hỏi thêm, không cho đặt lịch thường |
| D | "Đây là giấy hẹn của mẹ bạn (mẫu GH-2). Hãy đặt lịch tái khám theo giấy hẹn này." | App đọc đúng bác sĩ và ngày hẹn, người thử kiểm tra rồi tạo phiếu. Ghi: người thử có tin thông tin app đọc không, có sửa gì không |

**Chỉ số ghi cho nhiệm vụ A:** số thao tác (app tự đếm) và thời gian (bấm giờ) để có lịch. So với MyVinmec làm cùng nhiệm vụ: số ngày phải thử và thời gian (xem `01-phong-van`, IMG_4760).

## 2. Kết quả

| Người thử | Bối cảnh (không định danh) | Nhiệm vụ | Làm gì | Gặp gì | Trích dẫn | Số thao tác / thời gian | Sửa gì sau đó | Phiên bản |
|---|---|---|---|---|---|---|---|---|
| T1 | Chưa thử | A | | | | | | v0.1 |
| T1 | Chưa thử | B | | | | | | v0.1 |
| T1 | Chưa thử | C | | | | | | v0.1 |
| T2 | Chưa thử | A | | | | | | |
| T2 | Chưa thử | B | | | | | | |
| T2 | Chưa thử | C | | | | | | |
| T3 | Chưa thử | A | | | | | | |
| T3 | Chưa thử | B | | | | | | |
| T3 | Chưa thử | C | | | | | | |

## 3. Tổng hợp sau khi thử

- Điều người thử làm được ngay:
- Chỗ người thử khựng lại:
- Đã sửa (ghi vào `CHANGELOG.md`):
