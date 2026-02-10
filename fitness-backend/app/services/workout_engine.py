# app/services/workout_engine.py
from __future__ import annotations
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models_fitness import (
    ProgramTemplate,
    ProgramDayTemplate,
    ProgramWeekTemplate,
    RestDayTemplate,
)

DOW = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]  # 1..7 -> mon..sun

def _normalize_goal(goal: Optional[str]) -> str:
    g = (goal or "").strip().lower()
    if g in {"build muscle", "muscle_gain", "muscle", "bulk"}:
        return "muscle_gain"
    if g in {"lose fat", "fat_loss", "cut"}:
        return "fat_loss"
    if g in {"maintain", "maintenance", "recomp"}:
        return "recomp"
    return "recomp"

def _normalize_experience(exp: Optional[str]) -> str:
    e = (exp or "beginner").strip().lower()
    if e not in {"beginner", "intermediate", "advanced"}:
        return "beginner"
    return e

def _ensure_7_days(week_workouts: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    rest = {"focus": "Rest", "details": [], "coachNote": "Walk 20–30 min or 10 min mobility."}
    out: Dict[str, Dict[str, Any]] = {}
    for k in DOW:
        out[k] = week_workouts.get(k) or rest
    return out

def _pick_program(db: Session, goal: str, level: str) -> Optional[ProgramTemplate]:
    prog = (
        db.query(ProgramTemplate)
        .filter(
            ProgramTemplate.goal == goal,
            ProgramTemplate.level == level,
            ProgramTemplate.is_active.is_(True),
        )
        .order_by(ProgramTemplate.id.asc())
        .first()
    )
    if prog:
        return prog

    prog = (
        db.query(ProgramTemplate)
        .filter(
            ProgramTemplate.goal == goal,
            ProgramTemplate.is_active.is_(True),
        )
        .order_by(ProgramTemplate.id.asc())
        .first()
    )
    return prog

def build_week_workouts(db: Session, goal: Optional[str], experience: Optional[str]) -> Dict[str, Dict[str, Any]]:
    g = _normalize_goal(goal)
    e = _normalize_experience(experience)

    prog = _pick_program(db, g, e)
    if not prog:
        return _ensure_7_days({})

    week_rows = (
        db.query(ProgramWeekTemplate)
        .filter(ProgramWeekTemplate.program_id == prog.id)
        .all()
    )
    by_weekday = {w.weekday: w for w in week_rows}

    out: Dict[str, Dict[str, Any]] = {}

    for idx, key in enumerate(DOW, start=1):
        w = by_weekday.get(idx)
        if not w:
            out[key] = {"focus": "Rest", "details": [], "coachNote": "Recovery / light mobility."}
            continue

        if getattr(w, "is_rest", False):
            out[key] = {"focus": "Rest", "details": [], "coachNote": "Active recovery or easy walk."}
            continue

        day: Optional[ProgramDayTemplate] = (
            db.query(ProgramDayTemplate)
            .filter(
                ProgramDayTemplate.program_id == prog.id,
                ProgramDayTemplate.day_number == w.day_number,
            )
            .one_or_none()
        )

        if not day:
            out[key] = {"focus": "Rest", "details": [], "coachNote": "Recovery / light mobility."}
            continue

        details = getattr(day, "details_json", []) or []
        coach_note = getattr(day, "coach_note", "") or ""

        out[key] = {
            "focus": day.name or "Training",
            "details": details,
            "coachNote": coach_note,
        }

    return _ensure_7_days(out)
