# Báo cáo xác định nhu cầu (Need Statement)

Đặt lịch tái khám hộ người thân với đúng bác sĩ đang theo dõi người bệnh

| Thông tin tài liệu | |
|---|---|
| Dự án | Vinmec Exploration Sprint · Bài tập 1 tuần |
| Phương pháp | Need statement theo Biodesign (phương pháp đổi mới y tế của Đại học Stanford), gồm problem, population, outcome |
| Phiên bản · Ngày | 1.0 · 19/10/2026 |
| Dữ liệu đầu vào | 3 phỏng vấn ẩn danh (P1–P3), kiểm thử ứng dụng MyVinmec và chatbot MIA trong ứng dụng, 1 tổng quan hệ thống |
| Thuật ngữ | Xem `../THUAT-NGU.md` |

---

## Tóm tắt

Nhu cầu trọng tâm của bài tập là: người nhà khó đặt được lịch tái khám với đúng bác sĩ đã theo dõi người thân của mình. Trong phỏng vấn, P1 chấm khâu tái khám khó chịu ở mức cao nhất (5/5) vì không chọn lại được bác sĩ cũ, còn P2 không biết bác sĩ nào còn lịch gần nên chọn bác sĩ đầu tiên cho nhanh. Khi kiểm thử MyVinmec, nguyên nhân hiện rõ hơn: ứng dụng chỉ cho xem lịch trống theo từng ngày, và chatbot MIA không cung cấp thông tin lịch trống.

Giả thuyết ban đầu "người bệnh khó chọn đúng chuyên khoa" bị bác bỏ, vì cả 3 người đều tự chấm mức chắc chắn 4/5. Outcome (kết quả mong muốn) được chọn là thời gian và số lần thao tác để có lịch, đo được trên cả ứng dụng hiện tại lẫn prototype (bản mẫu thử nghiệm). Baseline (số liệu nền) chưa được đo định lượng, đây là giới hạn chính của báo cáo.

---

## 1. Need statement

> **Cách để giảm thời gian và số lần thao tác cần thiết để đặt lịch tái khám với đúng bác sĩ đang theo dõi người bệnh, cho người nhà đặt lịch hộ người thân (cha mẹ, ông bà), trong bối cảnh không biết bác sĩ đó còn trống lịch vào ngày nào, phải dò từng ngày hoặc chấp nhận một bác sĩ khác.**

| Thành phần | Nội dung | Căn cứ |
|---|---|---|
| Population (nhóm người dùng) | Người nhà, 25–40 tuổi, đặt lịch tái khám hộ cha mẹ, ông bà | Cả 3 lần đặt lịch gần nhất của P1–P3 đều là đặt hộ người thân. P2: người lớn tuổi "gần như không tự dùng được" app |
| Problem (vấn đề) | Không biết bác sĩ cũ còn trống lịch vào ngày nào. Người đặt phải dò từng ngày trên ứng dụng, hoặc để tổng đài tự xếp bác sĩ khác | Bằng chứng từ phỏng vấn, ứng dụng và chatbot (mục 2) |
| Outcome (kết quả mong muốn) | Giảm thời gian và số lần thao tác để có một lịch tái khám với đúng bác sĩ cũ | Đo được với mọi giải pháp, không phụ thuộc cách làm (mục 3) |

Kiểm tra tiêu chí "không chứa giải pháp": câu chỉ mô tả người dùng, vấn đề và kết quả cần đạt, không nhắc tới công nghệ, tính năng hay kênh cụ thể nào.

## 2. Bằng chứng

### 2.1. Từ phỏng vấn: nhu cầu

| Mã | Bằng chứng | Loại |
|---|---|---|
| P1 câu 1b, 3 | Tái khám là khâu khó chịu nhất (5/5): "người bệnh không được chủ động lựa chọn lại bác sĩ đã khám cho mình trong lần đầu tiên". Lần đầu, bác sĩ do bệnh viện sắp xếp | Trải nghiệm thật (qua tổng đài) |
| P1 câu 12 | Nếu sửa một điều: chọn được bác sĩ đã khám và điều trị lần trước khi tái khám | Ý kiến |
| P2 câu 11, 11b | Khựng lại ở bước chọn bác sĩ vì "không biết ai phù hợp và ai còn lịch gần". Khi thử thao tác: "Thôi mình chọn bác sĩ đầu tiên cho nhanh" | Trải nghiệm thật (app bệnh viện khác) |
| P2 câu 1b | "Bác sĩ dặn lịch tái khám nhưng mình phải tự nhớ để đặt lại" | Trải nghiệm thật |

### 2.2. Từ kiểm thử MyVinmec và MIA: cơ chế gây khó khăn

| Nguồn | Quan sát | Ảnh |
|---|---|---|
| Luồng đặt lịch | Sau khi chọn đúng bác sĩ, người dùng chỉ chọn được từng ngày. Ngày đã kín hiện thông báo "Hiện tại không có lịch trống". Không có màn hình tổng quan các ngày còn trống | `../01-phong-van/screenshots/IMG_4760.jpg` |
| Hồ sơ bác sĩ | Không hiển thị lịch trống. Mục "Giải thưởng và ghi nhận" hiện lỗi kỹ thuật thô | `../01-phong-van/screenshots/IMG_4761.jpg` |
| Chatbot MIA | Với tài khoản chưa có lịch sử khám, MIA chỉ hướng dẫn gọi tổng đài hoặc tự tìm tên bác sĩ. Không cung cấp lịch trống | `../01-phong-van/screenshots/M1.jpg` |
| Chatbot MIA | Từ chối câu hỏi về lịch và mức đông của khoa | `../01-phong-van/screenshots/M7.jpg` |

### 2.3. Từ tài liệu: vì sao "đúng bác sĩ" quan trọng

Tổng quan hệ thống (nghiên cứu tổng hợp có phương pháp các nghiên cứu cùng chủ đề) trên tạp chí BMJ Open (2018) gồm 22 nghiên cứu. 18 nghiên cứu ghi nhận tỷ lệ tử vong thấp hơn có ý nghĩa thống kê khi người bệnh được khám liên tục với cùng một bác sĩ. Hiệu ứng thấy ở cả bác sĩ đa khoa lẫn chuyên khoa. Đây là nghiên cứu quan sát, chỉ cho thấy mối liên quan, chưa chứng minh nhân quả. Chi tiết ở `../04-best-practice/best-practice.md`.

### 2.4. Đánh giá độ mạnh của bằng chứng

| Thành phần | Độ mạnh | Nhận xét |
|---|---|---|
| Nhu cầu "đúng bác sĩ cũ" | Trung bình | 2/3 người có trải nghiệm thật, ở hai kênh khác nhau (tổng đài, app) |
| Cơ chế "phải dò từng ngày" | Trung bình – thấp | Do người thực hiện tự kiểm thử trên MyVinmec, chưa quan sát người dùng thật |
| Tầm quan trọng lâm sàng | Trung bình | Tổng quan hệ thống, nghiên cứu quan sát |

## 3. Chỉ số đo outcome

| Chỉ số | Cách đo | Số liệu nền (baseline) |
|---|---|---|
| Số lần chọn ngày cho tới khi thấy lịch trống đầu tiên của bác sĩ cũ | Đếm khi thực hiện cùng một nhiệm vụ | Chưa đo định lượng trên MyVinmec. Ghi nhận định tính: "mất thời gian trong việc tìm lịch" |
| Thời gian từ khi mở ứng dụng tới màn hình xác nhận | Bấm giờ | Chưa đo. P2 tự kể khoảng 10–15 phút (ứng dụng của bệnh viện khác, có người hướng dẫn) |
| Tỷ lệ lần tái khám đặt được đúng bác sĩ cũ | Dữ liệu vận hành của bệnh viện | Không có quyền truy cập |

## 4. Các phương án đã cân nhắc

| Phương án | Kết luận | Lý do |
|---|---|---|
| Người bệnh khó chọn đúng chuyên khoa | Loại | Cả 3 người chấm mức chắc chắn 4/5. Giả thuyết bị bác bỏ |
| Gánh nặng khi đặt hộ người thân (D2) | Không chọn làm trọng tâm | Chỉ P2 có trải nghiệm thật. P1 thấy đặt hộ "không nhiều khác biệt" |
| Phải tự nhớ lịch tái khám (D6) | Không chọn làm trọng tâm | Chỉ P2 có trải nghiệm thật. Theo MIA, ứng dụng đã nhắc các lịch đã đặt (chưa kiểm chứng) |
| Thời gian chờ và thủ tục tại bệnh viện (D3, D4) | Ngoài phạm vi | Nguyên nhân thuộc vận hành bệnh viện, nằm ngoài khoảnh khắc đặt lịch |

## 5. Giới hạn

- Cỡ mẫu nhỏ: 3 người quen của người thực hiện, mỗi buổi 13–18 phút.
- Chưa người tham gia nào dùng MyVinmec. Bằng chứng về ứng dụng đến từ một lần tự kiểm thử bằng tài khoản mới.
- Điểm đau của P1 xuất phát từ kênh tổng đài, không phải ứng dụng.
- Chưa có số liệu nền định lượng cho outcome.

## 6. Tài liệu liên quan

| Tài liệu | Nội dung |
|---|---|
| `../01-phong-van/insight.md` | Tổng hợp insight, affinity map (gom ghi chép theo chủ đề), giả thuyết bị bác bỏ |
| `../01-phong-van/phan-tich-insight.md` | Danh mục điểm đau D1–D7, kịch bản kiểm thử ứng dụng |
| `../01-phong-van/myvinmec-trial.md` | Kết quả kiểm thử MyVinmec và MIA |
| `../02-journey-map/journey-map.md` | Journey map của khoảnh khắc đặt lịch tái khám |
