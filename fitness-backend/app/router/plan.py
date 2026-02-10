# app/routers/plan.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.db import get_db
from app.services.plan_builder import get_or_build_current_week, slice_today
from app.services.fitness_blocks import get_today_blocks
from app.models import UserProfile  # to read goal/experience for slug

router = APIRouter(prefix="/plan", tags=["plan"])

def _norm_goal(g: str | None) -> str:
    g = (g or "").strip().lower()
    if g in {"build muscle", "muscle_gain", "muscle", "bulk"}:
        return "muscle_gain"
    if g in {"lose fat", "fat_loss", "cut"}:
        return "fat_loss"
    if g in {"performance", "athletic"}:
        return "performance"
    return "recomp"

def _norm_level(lv: str | None) -> str:
    lv = (lv or "beginner").strip().lower()
    return lv if lv in {"beginner","intermediate","advanced"} else "beginner"

def _program_slug_for(db: Session, user_id: str) -> str:
    prof = db.query(UserProfile).filter_by(user_id=user_id).one_or_none()
    if not prof:
        return "muscle_gain_beginner"  # safe default
    g = _norm_goal(prof.goal)
    lv = _norm_level(prof.experience_level)
    # this matches the slug seeded by app/seed_fitness.py, e.g. "muscle_gain_beginner"
    return f"{g}_{lv}"

@router.post("/generate-week")
def generate_week(userId: str, db: Session = Depends(get_db)):
    # get_or_build_current_week should internally call the updated workout engine
    plan = get_or_build_current_week(db, userId, date.today())
    return {
        "daily_targets": plan.daily_targets,
        "week_meals": plan.week_meals,
        "week_workouts": plan.week_workouts,
        "grocery_list": plan.grocery_list,
        "week_start_date": str(plan.week_start_date),
    }

@router.get("/current")
def current(
    userId: str,
    db: Session = Depends(get_db),
    # allow override for debugging, but default to derived slug:
    programSlug: str | None = None,
):
    today = date.today()
    plan = get_or_build_current_week(db, userId, today)
    payload = slice_today(plan, today)

    # 🔑 derive the correct program slug from the user’s profile
    slug = programSlug or _program_slug_for(db, userId)

    # enrich with warmup/cooldown/rest using the RIGHT slug
    blocks = get_today_blocks(db, slug, today)
    payload["is_rest_day"] = blocks["is_rest"]
    payload["warmup"] = blocks["warmup"]
    payload["cooldown"] = blocks["cooldown"]
    payload["rest_recovery"] = blocks["rest"]
    payload["workout_title"] = blocks["title"]
    payload["workout_focus"] = blocks["focus"]
    return payload
