"""Prototype: người nhà đặt lịch tái khám hộ người thân với đúng bác sĩ cũ.

Chạy: streamlit run app.py
Dữ liệu giả trong mock-data/. Không phải sản phẩm của Vinmec.
"""

import datetime as dt
from collections import defaultdict

import streamlit as st

import core

st.set_page_config(page_title="Đặt lịch tái khám (prototype)", page_icon="🗓️")

FOOTER = "Prototype học tập, dữ liệu giả, không phải sản phẩm của Vinmec, không tư vấn y khoa."
DEFAULT_WINDOW_DAYS = 30

ss = st.session_state
ss.setdefault("step", "home")
ss.setdefault("clicks", 0)


def today() -> dt.date:
    return dt.date.today()


def go(step: str, **kw):
    ss.clicks += 1
    ss.step = step
    ss.update(kw)


def reset():
    for k in list(ss.keys()):
        del ss[k]


def start_booking(doctor: dict, patient: str, start: dt.date, end: dt.date, tod: str = "", source: str = ""):
    go("availability", doctor=doctor, patient=patient or "Người thân",
       start=start, end=end, tod=tod, source=source)


def footer():
    st.divider()
    st.caption(FOOTER)


# ------------------------------------------------------------------ màn hình
def screen_home():
    st.title("🗓️ Đặt lịch tái khám hộ người thân")
    st.write("Đặt lại với **đúng bác sĩ đã khám lần trước**, thấy ngay các ngày bác sĩ còn trống.")

    st.subheader("Phiếu tái khám bác sĩ đã hẹn")
    st.caption("Mô phỏng: bác sĩ tạo phiếu ngay sau buổi khám, phiếu gắn sẵn bác sĩ và khoảng thời gian.")
    for t in core.TICKETS:
        doc = core.DOCTOR_BY_ID[t["doctor_id"]]
        s, e = dt.date.fromisoformat(t["window_start"]), dt.date.fromisoformat(t["window_end"])
        with st.container(border=True):
            st.markdown(f"**{t['patient']}** · {doc['title']} {doc['name']} · {doc['department']}")
            st.caption(f"Tái khám trong khoảng {s:%d/%m} – {e:%d/%m/%Y}. {t['note']}")
            if st.button("Xem lịch trống và đặt", key=f"ticket_{t['id']}"):
                start_booking(doc, t["patient"], s, e, source=f"Phiếu {t['id']}")
                st.rerun()

    st.subheader("Chưa có phiếu? Tạo phiếu từ giấy hẹn")
    st.caption("Dán nội dung giấy hẹn tái khám (in hoặc chép tay). Ứng dụng bỏ các dòng có họ tên, "
               "chẩn đoán, đơn thuốc trước khi đọc, rồi chỉ lấy bác sĩ và ngày hẹn.")
    cols = st.columns(len(core.SLIPS))
    for c, sl in zip(cols, core.SLIPS):
        c.button(f"Mẫu {sl['id']}", key=f"slip_sample_{sl['id']}", help=sl["label"],
                 on_click=lambda t=sl["text"]: ss.update(slip=t))
    slip = st.text_area("Nội dung giấy hẹn (dữ liệu giả)", key="slip", height=150)
    if st.button("Tạo phiếu tái khám", key="slip_go") and slip.strip():
        clean, _ = core.redact(slip)
        flag = core.red_flag(clean)
        if flag:
            go("emergency", flag=flag)
            st.rerun()
        data, mode, removed = core.read_slip(slip, today())
        go("slip_review", slip_data=data, mode=mode, removed=removed)
        st.rerun()

    st.subheader("Hoặc nhập yêu cầu")
    text = st.text_area(
        "Bạn muốn đặt lịch thế nào?",
        key="req",
        placeholder="Ví dụ: đặt tái khám cho bố với bác sĩ Trần Minh An khoảng giữa tháng 11, buổi sáng",
    )
    if st.button("Tìm lịch", key="go", type="primary") and text.strip():
        # 1. Kiểm tra dấu hiệu khẩn cấp TRƯỚC mọi bước khác.
        flag = core.red_flag(text)
        if flag:
            go("emergency", flag=flag)
            st.rerun()
        # 2. Trích xuất yêu cầu (LLM, dự phòng bằng luật).
        data, mode = core.extract(text, today())
        ss.mode = mode
        ss.extracted = data
        # 3. Tìm bác sĩ, không đoán khi không chắc.
        doc, suggestions = core.match_doctor(data["doctor_name"], data["department"])
        start = _parse(data["earliest_date"]) or today() + dt.timedelta(days=1)
        end = _parse(data["latest_date"]) or start + dt.timedelta(days=DEFAULT_WINDOW_DAYS)
        if doc:
            start_booking(doc, data["patient"], start, end, data["preferred_time_of_day"], "Yêu cầu tự do")
        else:
            go("not_found", suggestions=suggestions, start=start, end=end,
               patient=data["patient"], tod=data["preferred_time_of_day"])
        st.rerun()


def _parse(s: str):
    try:
        return dt.date.fromisoformat(s) if s else None
    except ValueError:
        return None


def mode_badge():
    mode = ss.get("mode")
    if mode == "rules":
        st.caption("⚙️ Đọc bằng luật: thông tin đã đủ rõ nên không cần gọi AI, không gửi dữ liệu ra ngoài.")
    elif mode == "fallback":
        st.caption("⚙️ Chế độ không dùng AI: luật chưa đọc đủ thông tin và không gọi được AI "
                   "(không có API key hoặc AI lỗi). Bạn hãy kiểm tra và bổ sung.")
    elif mode == "ai":
        st.caption(f"🤖 Luật chưa đọc đủ nên đã nhờ AI ({core.MODEL}) đọc. "
                   "AI chỉ trích thông tin lịch hẹn, không tư vấn y khoa.")


def screen_slip_review():
    mode_badge()
    data = ss.slip_data
    st.title("Kiểm tra phiếu tái khám")
    st.caption(f"Đã bỏ {ss.removed} dòng có thông tin cá nhân hoặc sức khỏe trước khi đọc. "
               "Ứng dụng không đọc chẩn đoán hay đơn thuốc.")
    doc, suggestions = core.match_doctor(data["doctor_name"], data["department"])
    options = ([doc] if doc else suggestions) or core.DOCTORS
    labels = [f"{d['title']} {d['name']} · {d['department']}" for d in options]
    if doc:
        st.success(f"Đọc được bác sĩ: **{labels[0]}**")
    elif data["doctor_name"]:
        st.warning(f"Đọc được tên **{data['doctor_name']}** nhưng chưa chắc là bác sĩ nào. Bạn hãy chọn đúng bác sĩ.")
    else:
        st.warning("Chưa đọc được tên bác sĩ. Bạn hãy chọn bác sĩ đã khám.")
    pick = st.selectbox("Bác sĩ đã khám", range(len(options)), format_func=lambda i: labels[i], key="slip_doc")
    target = core.slip_target(data, today())
    if target:
        st.write(f"Ngày hẹn tái khám đọc được: **{target:%d/%m/%Y}**")
    else:
        st.warning("Chưa đọc được ngày hẹn. Bạn hãy chọn ngày bác sĩ hẹn.")
    target = st.date_input("Ngày hẹn tái khám", value=target or today() + dt.timedelta(days=30),
                           format="DD/MM/YYYY", key="slip_date")
    patient = st.selectbox("Người khám", ["Bố", "Mẹ", "Ông", "Bà", "Người thân"], key="slip_patient")
    start, end = core.slip_window(target, today())
    st.caption(f"Ứng dụng sẽ tìm lịch trống từ {start:%d/%m} đến {end:%d/%m/%Y} và tạo nhắc lịch tái khám.")
    c1, c2 = st.columns(2)
    if c1.button("Đúng, tạo phiếu và xem lịch trống", key="slip_ok", type="primary"):
        start_booking(options[pick], patient, start, end, source="Giấy hẹn")
        st.rerun()
    if c2.button("Quay lại", key="back_slip"):
        reset()
        st.rerun()


def screen_emergency():
    st.error(
        f"### ⚠️ Có dấu hiệu cần cấp cứu\n"
        f"Câu bạn nhập có dấu hiệu nguy hiểm (*{ss.flag}*). **Đừng đặt lịch khám thường.**\n\n"
        f"Gọi cấp cứu **115** ngay hoặc đến cơ sở cấp cứu gần nhất."
    )
    st.link_button("📞 Gọi 115", "tel:115", type="primary")
    st.caption("If this is an emergency, call 115 now. Đây là cảnh báo an toàn, không phải chẩn đoán.")
    st.caption("Ứng dụng dừng luồng đặt lịch ở đây và không hỏi thêm thông tin.")
    if st.button("Quay lại", key="back_emergency"):
        reset()
        st.rerun()


def screen_not_found():
    mode_badge()
    name = ss.extracted.get("doctor_name") if ss.get("extracted") else ""
    same_name = name and ss.suggestions and all(
        core.unaccent(d["name"]).split()[-1] in core.unaccent(name).split() for d in ss.suggestions)
    if same_name:
        st.info(f"Có {len(ss.suggestions)} bác sĩ tên **{name}**. Bạn hãy chọn bác sĩ đã khám lần trước.")
    elif name:
        st.warning(f"Không tìm thấy bác sĩ **{name}** trong danh sách. Ứng dụng không tự đoán bác sĩ.")
    else:
        st.warning("Không tìm thấy tên bác sĩ trong yêu cầu. Bạn hãy chọn bác sĩ đã khám lần trước.")
    options = ss.suggestions or core.DOCTORS
    st.write("Có phải bạn muốn tìm:" if ss.suggestions else "Danh sách bác sĩ:")
    for d in options:
        if st.button(f"{d['title']} {d['name']} · {d['department']}", key=f"pick_{d['id']}"):
            start_booking(d, ss.patient, ss.start, ss.end, ss.tod, "Chọn lại bác sĩ")
            st.rerun()
    if st.button("Quay lại", key="back_nf"):
        reset()
        st.rerun()


def screen_availability():
    mode_badge()
    doc, start, end = ss.doctor, ss.start, ss.end
    st.title("Lịch trống của bác sĩ")
    st.markdown(f"**{doc['title']} {doc['name']}** · {doc['department']}  \n"
                f"Người khám: **{ss.patient}** · Khoảng mong muốn: {start:%d/%m} – {end:%d/%m/%Y}"
                + (f" · Buổi {ss.tod}" if ss.tod else ""))
    st.caption(doc["bio"])

    slots = core.free_slots(doc["id"], start, end, ss.tod)
    if slots:
        by_day = defaultdict(list)
        for s in slots:
            by_day[s["date"]].append(s["time"])
        st.success(f"Bác sĩ còn trống **{len(by_day)} ngày** ({len(slots)} giờ khám) trong khoảng này. Chọn một giờ:")
        for day, times in by_day.items():
            cols = st.columns([2] + [1] * 6)
            cols[0].markdown(f"**{core.fmt_date(day)}**")
            for i, t in enumerate(times[:6]):
                if cols[i + 1].button(t, key=f"slot_{day}_{t}"):
                    go("confirm", slot={"date": day, "time": t})
                    st.rerun()
    else:
        st.warning("Bác sĩ đã kín lịch trong khoảng này.")
        nxt = core.next_slots_after(doc["id"], end)
        if nxt:
            st.write("Các giờ trống gần nhất sau khoảng mong muốn:")
            for s in nxt:
                if st.button(f"{core.fmt_date(s['date'])} · {s['time']}", key=f"next_{s['date']}_{s['time']}"):
                    go("confirm", slot=s)
                    st.rerun()
        if st.button("🔔 Báo cho tôi khi có lịch sớm hơn", key="waitlist"):
            ss.clicks += 1
            ss.waitlisted = True
        if ss.get("waitlisted"):
            st.info(f"Đã đăng ký danh sách chờ (mô phỏng). Khi có người hủy lịch trong khoảng {start:%d/%m} – {end:%d/%m}, "
                    f"thông báo sẽ gửi tới **bạn (người đặt)** và **{ss.patient}** (SMS).")
    if st.button("Quay lại", key="back_av"):
        reset()
        st.rerun()


def screen_confirm():
    doc, slot = ss.doctor, ss.slot
    st.title("Xác nhận lịch tái khám")
    st.markdown(
        f"- **Người khám:** {ss.patient}\n"
        f"- **Bác sĩ:** {doc['title']} {doc['name']} ({doc['department']})\n"
        f"- **Thời gian:** {core.fmt_date(slot['date'])}/{slot['date'][:4]} lúc {slot['time']}\n"
        f"- **Thông báo gửi tới:** bạn (người đặt) + {ss.patient} (SMS)\n"
        f"- **Nhắc lịch:** tự động tạo, nhắc trước 1 ngày và sáng ngày khám"
    )
    if ss.get("done"):
        st.success("Đã đặt lịch (mô phỏng, không tạo lịch thật).")
        st.metric("Số thao tác từ đầu đến khi có lịch", ss.clicks)
        st.caption("So sánh với MyVinmec: phải chọn từng ngày để biết bác sĩ có trống không (xem 01-phong-van, IMG_4760).")
        if st.button("Đặt lịch khác", key="restart"):
            reset()
            st.rerun()
    else:
        c1, c2 = st.columns(2)
        if c1.button("Xác nhận (mô phỏng)", key="confirm", type="primary"):
            ss.clicks += 1
            ss.done = True
            st.rerun()
        if c2.button("Chọn giờ khác", key="back_cf"):
            go("availability")
            st.rerun()


SCREENS = {
    "home": screen_home,
    "emergency": screen_emergency,
    "not_found": screen_not_found,
    "slip_review": screen_slip_review,
    "availability": screen_availability,
    "confirm": screen_confirm,
}
SCREENS[ss.step]()
footer()
