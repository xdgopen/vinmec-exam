"""Kiểm thử không giao diện. Chạy: python -m pytest tests (hoặc python tests/test_app.py)."""
import datetime as dt
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.pop("ANTHROPIC_API_KEY", None)  # luôn test đường dự phòng không dùng AI

import core  # noqa: E402
from streamlit.testing.v1 import AppTest  # noqa: E402

APP = str(ROOT / "app.py")


def all_text(at):
    parts = [e.value for e in at.markdown] + [e.value for e in at.success] + [e.value for e in at.warning] \
        + [e.value for e in at.error] + [e.value for e in at.info] + [e.value for e in at.caption]
    return "\n".join(str(p) for p in parts)


def test_red_flag_rules():
    assert core.red_flag("Bố tôi đột nhiên đau ngực dữ dội, khó thở")
    assert core.red_flag("bo toi dau nguc, kho tho")
    assert core.red_flag("My father has chest pain")
    assert core.red_flag("đặt tái khám cho bố với bác sĩ Trần Minh An") is None


def test_rules_extract():
    d = core.extract_with_rules("đặt tái khám cho bố với bác sĩ Trần Minh An khoảng giữa tháng 11, buổi sáng",
                                dt.date(2026, 10, 19))
    assert d["patient"] == "bố"
    assert d["doctor_name"] == "Trần Minh An"
    assert d["earliest_date"] == "2026-11-10" and d["latest_date"] == "2026-11-20"
    assert d["preferred_time_of_day"] == "sáng"


def test_ticket_flow_shows_many_days_then_confirm():
    at = AppTest.from_file(APP).run()
    at.button(key="ticket_PT-001").click().run()
    text = all_text(at)
    assert "còn trống" in text
    slot_buttons = [b for b in at.button if b.key and b.key.startswith("slot_")]
    days = {b.key.split("_")[1] for b in slot_buttons}
    assert len(days) >= 2, days
    slot_buttons[0].click().run()
    at.button(key="confirm").click().run()
    assert "Đã đặt lịch" in all_text(at)
    assert "người đặt" in all_text(at)


def test_ticket_no_slot_shows_next_and_waitlist():
    at = AppTest.from_file(APP).run()
    at.button(key="ticket_PT-002").click().run()
    assert "kín lịch" in all_text(at)
    assert any(b.key and b.key.startswith("next_") for b in at.button)
    at.button(key="waitlist").click().run()
    assert "danh sách chờ" in all_text(at)


def test_red_flag_input_shows_115_and_no_booking():
    at = AppTest.from_file(APP).run()
    at.text_area(key="req").input("Bố tôi đột nhiên đau ngực dữ dội, vã mồ hôi, khó thở. Nên đặt lịch hay làm gì?")
    at.button(key="go").click().run()
    assert "115" in all_text(at)
    assert at.session_state["step"] == "emergency"
    assert not any(b.key and b.key.startswith("slot_") for b in at.button)


def test_unknown_doctor_not_found():
    at = AppTest.from_file(APP).run()
    at.text_area(key="req").input("Tôi muốn đặt tái khám cho bố với bác sĩ Nguyễn Thanh David")
    at.button(key="go").click().run()
    assert "Không tìm thấy" in all_text(at)
    assert at.session_state["step"] == "not_found"


def test_free_text_known_doctor():
    at = AppTest.from_file(APP).run()
    at.text_area(key="req").input("đặt tái khám cho bố với bác sĩ Trần Minh An khoảng giữa tháng 11")
    at.button(key="go").click().run()
    assert at.session_state["step"] == "availability"
    assert "Đọc bằng luật" in all_text(at)          # câu đủ rõ: luật đọc được, không gọi AI


def test_match_doctor_short_name():
    assert core.match_doctor("An")[0]["id"] == "bs01"
    assert core.match_doctor("Minh An")[0]["id"] == "bs01"
    assert core.match_doctor("an")[0]["id"] == "bs01"          # không dấu, chữ thường
    assert core.match_doctor("Anh")[0]["id"] == "bs07"         # "Anh" không nhầm với "An"
    assert core.match_doctor("Hà")[0]["id"] == "bs03"
    assert core.match_doctor("Tran Minh An")[0]["id"] == "bs01"
    assert core.match_doctor("Nguyễn Thanh David")[0] is None
    assert core.match_doctor("Minh")[0] is None                 # thiếu tên gọi thì không đoán


def test_match_doctor_same_given_name(monkeypatch):
    extra = {"id": "bs99", "title": "BS", "name": "Lê Văn An", "department": "Nội tiết", "bio": ""}
    monkeypatch.setattr(core, "DOCTORS", core.DOCTORS + [extra])
    doc, sugg = core.match_doctor("An")
    assert doc is None and {d["id"] for d in sugg} == {"bs01", "bs99"}
    assert core.match_doctor("An", "Nội tiết")[0]["id"] == "bs99"  # khoa giúp phân biệt


def test_free_text_short_doctor_name():
    at = AppTest.from_file(APP).run()
    at.text_area(key="req").input("đặt tái khám cho mẹ với bác sĩ An")
    at.button(key="go").click().run()
    assert at.session_state["step"] == "availability"


def test_free_text_same_given_name_asks_to_choose(monkeypatch):
    extra = {"id": "bs99", "title": "BS", "name": "Lê Văn An", "department": "Nội tiết", "bio": ""}
    monkeypatch.setattr(core, "DOCTORS", core.DOCTORS + [extra])
    at = AppTest.from_file(APP).run()
    at.text_area(key="req").input("đặt tái khám cho mẹ với bác sĩ An")
    at.button(key="go").click().run()
    assert at.session_state["step"] == "not_found"
    assert "Có 2 bác sĩ tên" in all_text(at)
    assert "Không tìm thấy" not in all_text(at)


# ------------------------------------------------------------ v0.2: luật trước, AI sau; giấy hẹn
T = dt.date(2026, 10, 20)


def test_rules_fixes_and_relative_dates():
    d = core.extract_with_rules("bác sĩ dặn 3 tháng nữa tái khám, đặt giúp bà", T)
    assert d["patient"] == "bà"                      # trước đây bị đọc thành "ba"
    assert d["doctor_name"] == ""                    # "dặn" không phải tên bác sĩ
    assert d["earliest_date"] == "2027-01-13" and d["latest_date"] == "2027-01-27"
    d = core.extract_with_rules("cho mẹ tái khám tuần sau với bác sĩ an", T)
    assert (d["earliest_date"], d["latest_date"]) == ("2026-10-26", "2026-11-01")
    d = core.extract_with_rules("tái khám tim mạch cho bố vào tháng sau", T)
    assert (d["earliest_date"], d["latest_date"]) == ("2026-11-01", "2026-11-30")
    assert core.extract_with_rules("đặt cho ba với bs Bảo", T)["doctor_name"] == "Bảo"


def test_rules_first_ai_only_when_needed(monkeypatch):
    calls = []
    monkeypatch.setattr(core, "get_api_key", lambda: "fake-key")
    def fake_llm(text, today, key):
        calls.append(text)
        return core.validate({"patient": "bố", "doctor_name": "Trần Minh An", "earliest_date": "2026-11-02",
                              "latest_date": "2026-11-08"})
    monkeypatch.setattr(core, "extract_with_llm", fake_llm)
    data, mode = core.extract("tái khám cho bố với bác sĩ Trần Minh An giữa tháng 11", T)
    assert mode == "rules" and calls == []           # đủ thông tin: không gửi gì cho AI
    data, mode = core.extract("bố cần gặp lại bác sĩ An sau đợt điều trị", T)
    assert mode == "ai" and len(calls) == 1          # luật thiếu ngày: mới gọi AI


def test_redact_removes_identity_and_health_lines():
    clean, removed = core.redact(core.SLIPS[0]["text"])
    assert removed == 3
    for bad in ("Nguyễn Văn A", "1962", "Chẩn đoán"):
        assert bad not in clean
    assert "Trần Minh An" in clean and "12/11/2026" in clean


def test_read_slip_samples_with_rules():
    data, mode, _ = core.read_slip(core.SLIPS[0]["text"], T)
    assert mode == "rules" and core.match_doctor(data["doctor_name"], data["department"])[0]["id"] == "bs01"
    assert core.slip_target(data, T) == dt.date(2026, 11, 12)
    assert core.slip_window(dt.date(2026, 11, 12), T) == (dt.date(2026, 11, 5), dt.date(2026, 11, 19))
    data, mode, _ = core.read_slip(core.SLIPS[1]["text"], T)
    assert mode == "rules" and core.match_doctor(data["doctor_name"], data["department"])[0]["id"] == "bs03"
    assert core.slip_target(data, T) == dt.date(2026, 11, 20)   # khám 20/10 + 1 tháng


def test_read_slip_hard_case_needs_ai(monkeypatch):
    monkeypatch.setattr(core, "get_api_key", lambda: None)
    data, mode, _ = core.read_slip(core.SLIPS[2]["text"], T)
    assert mode == "fallback" and core.slip_target(data, T) is None   # luật không hiểu ngày hẹn
    sent = []
    monkeypatch.setattr(core, "get_api_key", lambda: "fake-key")
    def fake_slip_llm(text, today, key):
        sent.append(text)
        return {"doctor_name": "Nam", "department": "Tim mạch", "visit_date": "", "appointment_date": "2026-12-03",
                "follow_up_after_days": 0, "_offset": None}
    monkeypatch.setattr(core, "slip_with_llm", fake_slip_llm)
    data, mode, _ = core.read_slip(core.SLIPS[2]["text"], T)
    assert mode == "ai" and core.slip_target(data, T) == dt.date(2026, 12, 3)
    assert "Người bệnh" not in sent[0]               # AI chỉ nhận văn bản đã bỏ thông tin cá nhân


def test_slip_flow_in_app():
    at = AppTest.from_file(APP).run()
    at.button(key="slip_sample_GH-1").click().run()
    at.button(key="slip_go").click().run()
    assert at.session_state["step"] == "slip_review"
    assert "Trần Minh An" in all_text(at)
    at.button(key="slip_ok").click().run()
    assert at.session_state["step"] == "availability"
    assert at.session_state["source"] == "Giấy hẹn"


def test_slip_with_red_flag_goes_to_emergency():
    at = AppTest.from_file(APP).run()
    at.text_area(key="slip").input("Bác sĩ: Trần Minh An\nHôm nay bố bị đau ngực dữ dội")
    at.button(key="slip_go").click().run()
    assert at.session_state["step"] == "emergency"


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__, "-q"]))
