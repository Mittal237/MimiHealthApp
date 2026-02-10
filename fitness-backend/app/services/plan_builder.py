from __future__ import annotations
from datetime import date, timedelta
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.models import User, UserProfile, WeeklyPlan
from app.models_fitness import ProgramTemplate
from app.services.calculations import compute_daily_targets
from app.services.workout_engine import build_week_workouts
from app.services.meal_engine import build_week_meals, build_grocery_list

DOW_KEYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

def _monday(d: date) -> date:
    return d - timedelta(days=d.weekday())

def _safe_goal(goal: str | None) -> str:
    g = (goal or "").strip().lower()
    if g in {"build muscle", "muscle_gain", "muscle", "bulk"}:
        return "muscle_gain"
    if g in {"lose fat", "fat_loss", "cut"}:
        return "fat_loss"
    if g in {"performance", "athletic"}:
        return "performance"
    return "recomp"

def _safe_diet(diet: str | None) -> str:
    d = (diet or "nonveg").strip().lower()
    return d

def _resolve_experience(db: Session, goal: str, exp: str) -> str:
    slug = f"{goal}_{exp}"
    exists = db.query(ProgramTemplate.id).filter(ProgramTemplate.slug == slug).first()
    if exists:
        return exp

    beg_slug = f"{goal}_beginner"
    beg_exists = db.query(ProgramTemplate.id).filter(ProgramTemplate.slug == beg_slug).first()
    if beg_exists:
        return "beginner"

    return exp

def build_week_using_engines(db: Session, user_id: str, today: date) -> WeeklyPlan:
    user: User = db.query(User).filter_by(id=user_id).one()
    profile: UserProfile = db.query(UserProfile).filter_by(user_id=user_id).one()

    goal = _safe_goal(profile.goal)
    diet_type = _safe_diet(profile.diet_type)
    exp_raw = (profile.experience_level or "beginner").strip().lower()
    experience = _resolve_experience(db, goal, exp_raw)

    week_start = _monday(today)

    targets: Dict[str, Any] = compute_daily_targets(
        sex=profile.sex,
        age=profile.age,
        height_cm=profile.height_cm,
        weight_kg=profile.weight_kg,
        activity=profile.activity_level,
        goal=goal,
    )

    week_workouts: Dict[str, Any] = build_week_workouts(
        db=db,
        goal=goal,
        experience=experience,
    )

    week_meals: Dict[str, Any] = build_week_meals(
        db=db,
        goal=goal,
        diet_type=diet_type,
        fav_protein=profile.fav_protein
    )

    grocery = build_grocery_list(week_meals)

    plan = WeeklyPlan(
        user_id=user_id,
        week_start_date=week_start,
        daily_targets=targets,
        week_meals=week_meals,
        week_workouts=week_workouts,
        grocery_list=grocery,
        goal=goal, 
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


def get_or_build_current_week(db: Session, user_id: str, today: date) -> WeeklyPlan:
    week_start = _monday(today)

    plan = (
        db.query(WeeklyPlan)
        .filter(WeeklyPlan.user_id == user_id, WeeklyPlan.week_start_date == week_start)
        .one_or_none()
    )

    if plan:
        profile: UserProfile = db.query(UserProfile).filter_by(user_id=user_id).one()
        current_goal = _safe_goal(profile.goal)

        if plan.goal != current_goal:
            db.delete(plan)
            db.commit()
            plan = None

    if plan:
        return plan

    return build_week_using_engines(db, user_id, today)


def slice_today(plan: WeeklyPlan, today: date):
    key = DOW_KEYS[today.weekday()]
    return {
        "daily_targets": plan.daily_targets,
        "today_meals": plan.week_meals.get(key, []),
        "workout_today": plan.week_workouts.get(
            key,
            {"focus": "Rest", "details": [], "coachNote": "Rest up."},
        ),
        "week_meals": plan.week_meals,
        "week_workouts": plan.week_workouts,
        "grocery_list": plan.grocery_list,
    }
