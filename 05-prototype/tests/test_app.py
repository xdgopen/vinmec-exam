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
    assert "Chế độ không dùng AI" in all_text(at)


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


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__, "-q"]))
