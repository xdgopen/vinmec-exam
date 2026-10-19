"""Logic không phụ thuộc giao diện: kiểm tra dấu hiệu khẩn cấp, trích xuất yêu cầu,
tìm bác sĩ, tìm lịch trống. Tách riêng để test được mà không cần Streamlit."""

from __future__ import annotations

import calendar
import datetime as dt
import difflib
import json
import os
import re
import unicodedata
from pathlib import Path

BASE = Path(__file__).parent
DATA = BASE / "mock-data"
MODEL = "claude-sonnet-5-5"


def load(name: str):
    return json.loads((DATA / f"{name}.json").read_text(encoding="utf-8"))


DOCTORS = load("doctors")
SLOTS = load("slots")
TICKETS = load("tickets")
DOCTOR_BY_ID = {d["id"]: d for d in DOCTORS}


def unaccent(text: str) -> str:
    text = text.replace("đ", "d").replace("Đ", "D")
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", text.lower()).strip()


# ---------------------------------------------------------------- 1. Khẩn cấp
# Chạy TRƯỚC mọi bước khác (trước khi hỏi gì, trước khi gọi LLM).
# Bài học từ MIA: M5 bắt điền form trước khi hiện 115; M9 hỏi tiếng Anh thì không có 115.
RED_FLAGS_VI = [
    "đau ngực", "tức ngực", "đau thắt ngực", "khó thở", "thở dốc", "không thở được",
    "ngất", "bất tỉnh", "mất ý thức", "lơ mơ", "méo miệng", "yếu nửa người",
    "liệt nửa người", "nói đớ", "nói ngọng đột ngột", "co giật", "chảy máu không cầm",
    "nôn ra máu", "ho ra máu", "đi ngoài ra máu", "sốt cao cứng gáy", "cứng gáy",
    "đau đầu dữ dội", "phản vệ", "sưng môi lưỡi", "ngộ độc", "tự tử", "muốn chết",
]
RED_FLAGS_EN = [
    "chest pain", "can't breathe", "cannot breathe", "shortness of breath",
    "difficulty breathing", "unconscious", "fainted", "seizure", "stroke",
    "face drooping", "slurred speech", "severe bleeding", "vomiting blood",
    "suicide", "overdose", "anaphylaxis",
]
_RED_PATTERNS = [re.compile(r"\b" + re.escape(unaccent(k)) + r"\b") for k in RED_FLAGS_VI + RED_FLAGS_EN]


def red_flag(text: str) -> str | None:
    """Trả về từ khóa khẩn cấp đầu tiên tìm thấy, hoặc None."""
    norm = unaccent(text)
    for kw, pat in zip(RED_FLAGS_VI + RED_FLAGS_EN, _RED_PATTERNS):
        if pat.search(norm):
            return kw
    return None


# ---------------------------------------------------------------- 2. Trích xuất
SCHEMA = {
    "type": "object",
    "properties": {
        "patient": {"type": "string"},
        "doctor_name": {"type": "string"},
        "department": {"type": "string"},
        "earliest_date": {"type": "string"},
        "latest_date": {"type": "string"},
        "preferred_time_of_day": {"type": "string"},
        "is_follow_up": {"type": "boolean"},
    },
    "required": ["patient", "doctor_name", "department", "earliest_date",
                 "latest_date", "preferred_time_of_day", "is_follow_up"],
    "additionalProperties": False,
}


def system_prompt(today: dt.date) -> str:
    text = (BASE / "prompts" / "extract-system-prompt.md").read_text(encoding="utf-8")
    return text.replace("{today}", today.isoformat())


def get_api_key() -> str | None:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return key
    try:
        import streamlit as st
        return st.secrets.get("ANTHROPIC_API_KEY")
    except Exception:
        return None


def extract_with_llm(text: str, today: dt.date, api_key: str) -> dict:
    import anthropic

    client = anthropic.Anthropic(api_key=api_key)
    resp = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=system_prompt(today),
        messages=[{"role": "user", "content": text}],
        output_config={"effort": "low", "format": {"type": "json_schema", "schema": SCHEMA}},
    )
    if resp.stop_reason != "end_turn":
        raise ValueError(f"stop_reason={resp.stop_reason}")
    raw = next(b.text for b in resp.content if b.type == "text")
    return validate(json.loads(raw))


def validate(data: dict) -> dict:
    out = {k: data.get(k, "") for k in SCHEMA["properties"]}
    out["is_follow_up"] = bool(data.get("is_follow_up", True))
    for k in ("earliest_date", "latest_date"):
        try:
            if out[k]:
                dt.date.fromisoformat(out[k])
        except (TypeError, ValueError):
            out[k] = ""
    if out["preferred_time_of_day"] not in ("sáng", "chiều"):
        out["preferred_time_of_day"] = ""
    return out


PATIENTS = ["ông nội", "bà nội", "ông ngoại", "bà ngoại", "bố", "mẹ", "ba", "má",
            "ông", "bà", "vợ", "chồng", "con"]
STOPWORDS = {"khoang", "vao", "thang", "ngay", "luc", "cho", "giua", "dau", "cuoi",
             "tuan", "sang", "chieu", "o", "tai", "khoa", "nhe", "a", "di"}


def extract_with_rules(text: str, today: dt.date) -> dict:
    """Bộ trích xuất dự phòng khi không có API key hoặc LLM lỗi."""
    norm = unaccent(text)
    patient = next((p for p in PATIENTS if re.search(r"\b" + unaccent(p) + r"\b", norm)), "")

    doctor = ""
    m = re.search(r"(?:bác sĩ|bac si|bs\.?)\s+((?:[A-ZĐÀ-Ỹ][\wÀ-ỹ]*\s*){1,4})", text)
    if m:
        doctor = m.group(1).strip()
    else:
        m = re.search(r"(?:bác sĩ|bac si|bs\.?)\s+(\S+(?:\s+\S+){0,3})", text, re.IGNORECASE)
        if m:
            words = []
            for w in m.group(1).split():
                if unaccent(w) in STOPWORDS or re.search(r"\d", w):
                    break
                words.append(w)
            doctor = " ".join(words)

    department = ""
    for d in {d["department"] for d in DOCTORS}:
        if unaccent(d) in norm:
            department = d

    earliest = latest = ""
    dates = re.findall(r"\b(\d{1,2})/(\d{1,2})(?:/(\d{4}))?\b", text)
    parsed = []
    for dd, mm, yy in dates:
        try:
            parsed.append(dt.date(int(yy or today.year), int(mm), int(dd)))
        except ValueError:
            pass
    if parsed:
        earliest, latest = min(parsed).isoformat(), max(parsed).isoformat()
    else:
        m = re.search(r"(dau|giua|cuoi)?\s*thang\s*(\d{1,2})", norm)
        if m:
            month = int(m.group(2))
            year = today.year if month >= today.month else today.year + 1
            last = calendar.monthrange(year, month)[1]
            lo, hi = {"dau": (1, 10), "giua": (10, 20), "cuoi": (20, last)}.get(m.group(1), (1, last))
            earliest, latest = dt.date(year, month, lo).isoformat(), dt.date(year, month, hi).isoformat()

    tod = "sáng" if re.search(r"\bsang\b", norm) else "chiều" if re.search(r"\bchieu\b", norm) else ""
    return validate({"patient": patient, "doctor_name": doctor, "department": department,
                     "earliest_date": earliest, "latest_date": latest,
                     "preferred_time_of_day": tod, "is_follow_up": True})


def extract(text: str, today: dt.date) -> tuple[dict, str]:
    """Trả về (dữ liệu, chế độ). Chế độ là 'ai' hoặc 'rules'."""
    key = get_api_key()
    if key:
        try:
            return extract_with_llm(text, today, key), "ai"
        except Exception:
            pass
    return extract_with_rules(text, today), "rules"


# ---------------------------------------------------------------- 3. Tìm bác sĩ
def match_doctor(name: str, department: str = "") -> tuple[dict | None, list[dict]]:
    """Trả về (bác sĩ khớp, danh sách gợi ý). Không bao giờ tự đoán khi không chắc.

    Người nhà thường chỉ nhớ tên gọi ("bác sĩ An") hoặc tên đệm + tên ("bác sĩ Minh An"),
    nên khớp theo từ trước, rồi mới so gần đúng cả chuỗi để bắt lỗi chính tả.
    """
    if not name:
        return None, []
    q = unaccent(name)
    pool = [d for d in DOCTORS if not department or unaccent(d["department"]) == unaccent(department)] or DOCTORS

    # 1. Khớp đầy đủ.
    exact = [d for d in pool if unaccent(d["name"]) == q]
    if len(exact) == 1:
        return exact[0], []

    # 2. Khớp theo từ: mọi từ người dùng gõ đều có trong tên, và có tên gọi (từ cuối).
    q_tokens = q.split()
    by_token = []
    for d in pool:
        n_tokens = unaccent(d["name"]).split()
        if n_tokens[-1] in q_tokens and all(t in n_tokens for t in q_tokens):
            by_token.append(d)
    if len(by_token) == 1:
        return by_token[0], []
    if by_token:
        return None, by_token  # nhiều bác sĩ trùng tên: để người dùng chọn

    # 3. Gần đúng cả chuỗi (sai chính tả).
    scored = sorted(((difflib.SequenceMatcher(None, q, unaccent(d["name"])).ratio(), d) for d in pool),
                    key=lambda x: -x[0])
    best_score, best = scored[0]
    if best_score >= 0.92:
        return best, []
    return None, [d for s, d in scored[:3] if s >= 0.6]


# ---------------------------------------------------------------- 4. Lịch trống
def free_slots(doctor_id: str, start: dt.date, end: dt.date, tod: str = "") -> list[dict]:
    out = []
    for s in SLOTS:
        if s["doctor_id"] != doctor_id:
            continue
        d = dt.date.fromisoformat(s["date"])
        if start <= d <= end:
            if tod == "sáng" and s["time"] >= "12:00":
                continue
            if tod == "chiều" and s["time"] < "12:00":
                continue
            out.append(s)
    return out


def next_slots_after(doctor_id: str, after: dt.date, n: int = 3) -> list[dict]:
    return [s for s in SLOTS if s["doctor_id"] == doctor_id
            and dt.date.fromisoformat(s["date"]) > after][:n]


WEEKDAYS = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "CN"]


def fmt_date(iso: str) -> str:
    d = dt.date.fromisoformat(iso)
    return f"{WEEKDAYS[d.weekday()]} {d.day:02d}/{d.month:02d}"
