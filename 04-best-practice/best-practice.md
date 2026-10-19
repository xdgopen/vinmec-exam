# Báo cáo best practice quốc tế

**Đặt lịch tái khám với đúng bác sĩ**

| Thông tin tài liệu | |
|---|---|
| Dự án | Vinmec Exploration Sprint · Bài tập 1 tuần |
| Câu hỏi nghiên cứu | Các hệ thống y tế quốc tế giúp người bệnh (và người nhà) đặt lịch tái khám với đúng bác sĩ như thế nào? |
| Need statement liên quan | `../03-need-statement/need-statement.md` |
| Nguồn | 6 tài liệu, đã mở và đối chiếu số liệu, truy cập ngày 19/10/2026 (mục 5) |
| Phiên bản · Ngày | 1.0 · 19/10/2026 |
| Thuật ngữ | Xem `../THUAT-NGU.md` |

---

## Tóm tắt

Báo cáo chọn 3 cách làm ở nước ngoài, mỗi cách ứng với một bước trong journey map.

| Thực hành | Nơi áp dụng | Kết quả hoặc bằng chứng |
|---|---|---|
| Phiếu tái khám do bác sĩ tạo | Epic MyChart (ứng dụng cho người bệnh của hãng phần mềm bệnh án Epic), Mỹ | 17% lịch tái khám được người bệnh tự đặt online |
| Tự động mời nhận lịch trống sớm hơn | Epic Fast Pass, bệnh viện đại học UCSF (Mỹ) | Người bệnh được khám sớm hơn trung vị 14 ngày, nhưng chỉ 11% lời mời được chấp nhận (JMIR 2024) |
| Truy cập thay mặt người thân | NHS App (ứng dụng của hệ thống y tế công Anh) | Chưa có số liệu kết quả |

Bài học cho Vinmec gồm ba ý. Thứ nhất, hiển thị sẵn lịch trống của đúng bác sĩ trong khoảng thời gian tái khám. Thứ hai, gửi lời mời và thông báo cho cả người nhà, vì người từ 65 tuổi ít nhận lời mời qua app hơn. Thứ ba, chỉ cho đặt hộ khi người bệnh đồng ý.

Bằng chứng của cả ba ở mức thấp đến trung bình, và cả ba đều cần bệnh viện tích hợp dữ liệu hồ sơ và lịch khám.

---

## 1. Tổng quan ba best practice

| # | Best practice | Ở đâu | Giải quyết điểm đau nào | Bằng chứng |
|---|---|---|---|---|
| 1 | Phiếu tái khám do bác sĩ tạo (Scheduling Tickets) | Epic MyChart, nhiều hệ thống y tế ở Mỹ (UC Davis Health, Cleveland Clinic…) | D6 phải tự nhớ lịch tái khám, D1 đặt lại đúng bác sĩ | Báo cáo nội bộ UC Davis Health (2024), chưa có nghiên cứu độc lập |
| 2 | Tự động báo lịch trống sớm hơn (Fast Pass) | Epic MyChart, UCSF Health (Mỹ) | **Điểm đau chính:** phải dò từng ngày để tìm lịch trống | Nghiên cứu đoàn hệ hồi cứu (phân tích dữ liệu có sẵn) trên JMIR (2024), 60.660 lời mời |
| 3 | Truy cập thay mặt người thân (Family and carer access, còn gọi là proxy access) | NHS App (Anh) | D2 hệ thống chỉ nhận một người, người nhà đặt hộ | Trang hướng dẫn chính thức của NHS, chưa có số liệu kết quả |

Lý do cần giữ "đúng bác sĩ" khi tái khám: một tổng quan hệ thống trên BMJ Open (2018) gồm 22 nghiên cứu, trong đó 18 nghiên cứu ghi nhận tỷ lệ tử vong thấp hơn có ý nghĩa thống kê khi người bệnh được khám liên tục với cùng bác sĩ. Kết quả này thấy ở cả bác sĩ đa khoa lẫn chuyên khoa. Vì đều là nghiên cứu quan sát, kết quả chỉ cho thấy mối liên quan, chưa chứng minh nhân quả [5].

## 2. Chi tiết từng best practice

### BP1. Phiếu tái khám do bác sĩ tạo (Epic MyChart Scheduling Tickets)

| Mục | Nội dung |
|---|---|
| Làm gì | Khi bác sĩ chỉ định tái khám (hoặc xét nghiệm, chụp chiếu), MyChart tự tạo một "phiếu đặt lịch" trong tài khoản người bệnh, ở mục "Ready to Schedule" [1][2]. Người bệnh mở phiếu, trả lời vài câu hỏi rồi tự chọn giờ. Phiếu chỉ cho đặt những lịch bác sĩ đã yêu cầu [2]. Người chưa có tài khoản có thể nhận phiếu qua email [2]. Có thể vào danh sách chờ để lấy giờ sớm hơn [1] |
| Kết quả | Tại UC Davis Health, khi có phiếu, người bệnh tự đặt online 17% lịch tái khám và 46% lịch khám mới. Tự đặt mất khoảng 1 phút, gọi điện mất trung bình 7,2 phút. Lịch tự đặt có tỷ lệ không đến khám thấp hơn, nhưng bài không nêu con số [3] |
| Mức bằng chứng | Thấp: bản tin nội bộ của một hệ thống y tế, chưa qua bình duyệt |
| Áp dụng cho Vinmec | Thay lời dặn miệng "tái khám sau 3 tháng" (P2-1b) bằng một phiếu tái khám trong MyVinmec, do bác sĩ tạo ngay trong buổi khám, ghi sẵn tên bác sĩ và khoảng thời gian. Người nhà sẽ không phải tự nhớ lịch (D6) hay tìm lại tên bác sĩ (D1, M1). Hiện MyVinmec chỉ nhắc những lịch đã đặt (M4) |
| Không áp dụng nguyên được | (1) Cần tích hợp với hồ sơ bệnh án điện tử và thay đổi thao tác của bác sĩ cuối buổi khám, vượt phạm vi một prototype. (2) Chỉ 17% lịch tái khám được tự đặt online, đa số vẫn qua kênh khác. Ở Việt Nam, P1 và P3 vẫn chuộng tổng đài và người quen (D5), nên **phiếu phải dùng được cả khi gọi tổng đài**. (3) Các nguồn không nói rõ phiếu có luôn gắn với đúng bác sĩ cũ hay không |

### BP2. Tự động báo lịch trống sớm hơn (Epic Fast Pass)

| Mục | Nội dung |
|---|---|
| Làm gì | Người bệnh đã có lịch hẹn được đưa vào danh sách chờ. Khi có người hủy, hệ thống tự gửi lời mời qua MyChart để người bệnh nhận lịch sớm hơn. Người bệnh đồng ý thì lịch được đổi ngay, không cần gọi điện [4] |
| Kết quả | UCSF Health, 18/6/2022 đến 9/3/2023: 60.660 lời mời cho 21.978 lịch trống. Khoảng 11% lời mời được chấp nhận, tương ứng 30,5% lịch trống được lấp. 84,2% lịch đã nhận dẫn đến lần khám thật. Người bệnh được khám **sớm hơn trung vị 14 ngày**. Thêm 2.576 giờ khám [4] |
| Mức bằng chứng | Trung bình: nghiên cứu đoàn hệ hồi cứu, có bình duyệt, tại một trung tâm |
| Bài học ngược | Người từ 65 tuổi ít nhận lời mời hơn (OR, tức tỷ số chênh, 0,86). Người nói tiếng Trung còn ít nhận hơn (OR 0,62). Nhóm tác giả cảnh báo công cụ số có thể làm tăng bất bình đẳng trong tiếp cận [4] |
| Áp dụng cho Vinmec | Cách này giải quyết thẳng điểm đau chính: hệ thống chủ động báo khi bác sĩ cũ có lịch trống trong khoảng tái khám, người nhà không phải dò từng ngày (IMG_4760). Vì người lớn tuổi ít tự dùng, lời mời nên gửi cho người nhà đặt hộ, đúng nhóm người dùng trong need statement (P2: "với người lớn tuổi như ông thì app gần như không tự dùng được") |
| Không áp dụng nguyên được | (1) Cần dữ liệu lịch trống theo thời gian thực. MIA hiện không trả lời được câu hỏi về lịch (M7), có thể Vinmec chưa mở dữ liệu này cho kênh số. (2) 89% lời mời bị bỏ qua, nên không thể chỉ trông vào thông báo đẩy |

### BP3. Truy cập thay mặt người thân (NHS App family and carer access)

| Mục | Nội dung |
|---|---|
| Làm gì | Người nhà hoặc người chăm sóc được thao tác thay người bệnh trong NHS App. Tùy mức phòng khám cho phép, họ có thể đặt lịch khám, quản lý đơn thuốc định kỳ và xem kết quả xét nghiệm. Người nhà chuyển sang hồ sơ người thân qua Profile, mục Family and carer access [6] |
| Kiểm soát | Hai người phải đăng ký cùng một phòng khám bác sĩ đa khoa (GP surgery). Phòng khám xác minh danh tính, kiểm tra an toàn cho người dễ bị tổn thương (safeguarding) và xin đồng ý khi cần trước khi cấp quyền. Người nhà không tự đổi hay gỡ quyền được mà phải liên hệ phòng khám [6] |
| Kết quả | Trang chính thức không công bố số liệu. Đây là một thiết kế dịch vụ, chưa có bằng chứng định lượng |
| Áp dụng cho Vinmec | P2 muốn "một tài khoản quản lý hồ sơ người thân, kèm thông báo gửi đến cả hai người" (P2-12). MyVinmec đã có chức năng "Thêm hồ sơ" người thân (M3), nhưng thông báo và kết quả chỉ về máy người đặt (P2-6, P2-8). Điều nên học từ NHS: **quyền thay mặt phải được người bệnh đồng ý và thu hồi được**, không chỉ là một hồ sơ phụ trong tài khoản người nhà |
| Không áp dụng nguyên được | (1) NHS dựa vào việc người dân đăng ký cố định với một phòng khám, Việt Nam không có cơ chế này. (2) Thông tin sức khỏe là dữ liệu cá nhân nhạy cảm theo quy định bảo vệ dữ liệu cá nhân của Việt Nam (Nghị định 13/2023/NĐ-CP; cần kiểm tra văn bản hiện hành), nên phải có quy trình xin đồng ý rõ ràng. (3) Theo trang NHS, quyền thay mặt không áp dụng cho lịch khám ngoại trú ở bệnh viện, tức mô hình này mới dừng ở tuyến chăm sóc ban đầu |

## 3. Ghép lại thành bài học cho Vinmec

| Bước trong journey | Hiện trạng MyVinmec (kiểm thử 19/10) | Học từ |
|---|---|---|
| 1–2. Bác sĩ hẹn, người nhà tự nhớ | Chỉ dặn miệng. App chỉ nhắc lịch đã đặt (M4) | BP1: phiếu tái khám do bác sĩ tạo |
| 5. Tìm lại bác sĩ cũ | Phải tự nhớ tên. MIA không nhận ra tên sai (M1, M2) | BP1: phiếu ghi sẵn bác sĩ |
| **6. Tìm lịch trống** | Dò từng ngày (IMG_4760). MIA không trả lời về lịch (M7) | BP2: hệ thống chủ động báo lịch trống |
| 7–8. Đặt hộ, nhận thông báo | Có hồ sơ người thân, thông báo về máy người đặt (M3, P2-6) | BP3: quyền thay mặt có đồng ý, thông báo cho cả hai |

Prototype mô phỏng BP1 và BP2 bằng dữ liệu giả: một phiếu tái khám ghi bác sĩ cũ và khoảng thời gian, kèm danh sách các ngày bác sĩ đó còn trống. BP3 chỉ được đưa vào phần rủi ro và đạo đức (đồng ý, quyền thay mặt).

## 4. Giới hạn của phần nghiên cứu này

- BP1 và BP3 chưa có nghiên cứu độc lập đo kết quả. Chỉ BP2 có nghiên cứu đã bình duyệt.
- Cả ba đều đến từ hệ thống y tế có hồ sơ bệnh án điện tử tích hợp (Mỹ, Anh). Bài này chưa kiểm chứng mức độ tích hợp dữ liệu của Vinmec.
- Doctolib (Pháp) bị loại vì số liệu giảm tỷ lệ bỏ hẹn chỉ do chính công ty công bố.

## 5. Nguồn (truy cập 19/10/2026)

1. CRH (crh.org). *MyChart Ticket Scheduling for Follow-up Appointments*, 26/3/2026. https://www.crh.org/healthy-tomorrow/story/healthy-tomorrow/2026/03/26/new-visit-ticket-scheduling-in-mychart
2. Cleveland Clinic. *MyChart Appointment and Scheduling Troubleshooting*. https://my.clevelandclinic.org/resources/mychart-appointment-and-scheduling-troubleshooting
3. UC Davis Health. *Patients can now self-schedule new and follow-up visits with specialists*, 20/9/2024. https://health.ucdavis.edu/insideout/news/features/patients-can-now-self-schedule-new-and-follow-up-visits-with-specialists/2024/09
4. Ganeshan S, Liu AW, Kroeger A, et al. *An Electronic Health Record–Based Automated Self-Rescheduling Tool to Improve Patient Access: Retrospective Cohort Study.* J Med Internet Res 2024;26:e52071. doi:10.2196/52071. https://pmc.ncbi.nlm.nih.gov/articles/PMC10988365 *(Lưu ý: tóm tắt ghi 6.603 lời mời được chấp nhận, phần Kết quả ghi 6.703.)*
5. Pereira Gray DJ, Sidaway-Lee K, White E, Thorne A, Evans PH. *Continuity of care with doctors—a matter of life and death? A systematic review of continuity of care and mortality.* BMJ Open 2018;8(6):e021161. doi:10.1136/bmjopen-2017-021161. https://bmjopen.bmj.com/content/8/6/e021161
6. NHS. *Family and carer access* (NHS App help). https://www.nhs.uk/nhs-app/help/profile/family-and-carer-access/
