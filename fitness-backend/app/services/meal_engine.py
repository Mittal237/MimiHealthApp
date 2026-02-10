# app/services/meal_engine.py
from __future__ import annotations
from typing import Dict, List
from sqlalchemy.orm import Session
from app.models import MealLibrary

DOW = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

def _normalize_goal(goal: str | None) -> str:
    g = (goal or "").strip().lower()
    if g in {"muscle_gain", "build muscle", "muscle", "bulk"}:
        return "muscle_gain"
    if g in {"fat_loss", "lose fat", "cut"}:
        return "fat_loss"
    if g in {"performance", "athletic"}:
        return "performance"
    return "recomp"

def _normalize_diet(diet: str | None) -> str:
    d = (diet or "").strip().lower()

    if d in {"veg", "vegetarian"}:
        return "veg"

    if d in {"nonveg", "non-veg"}:
        return "nonveg"

    return "veg"

def _pick_breakfast(db: Session, goal: str, diet: str, fav: str | None = None) -> dict | None:
    fav = (fav or "").strip().lower()
    rows = (
        db.query(MealLibrary)
        .filter(
            MealLibrary.category == "breakfast",
            MealLibrary.diet_type == diet,
            MealLibrary.goal_flags.contains([goal]),
            MealLibrary.name.ilike("%egg%")
        )
        .all()
    )
    return _meal_to_json(rows[0]) if rows else None

def _pick_lunch(db: Session, goal: str, diet: str, fav: str | None = None) -> tuple[dict, dict]:
    """
    Return 2 lunch meals:
    - lunchA → first 3 days
    - lunchB → next 4 days
    If only 1 lunch exists → use it for both.
    """

    rows = (
        db.query(MealLibrary)
        .filter(
            MealLibrary.category == "lunch",
            MealLibrary.diet_type == diet,
            MealLibrary.goal_flags.contains([goal]),
        )
        .all()
    )

    if not rows:
        return None, None

    if len(rows) == 1:
        one = _meal_to_json(rows[0])
        return one, one

    # Use first 2 lunches
    lunchA = _meal_to_json(rows[0])
    lunchB = _meal_to_json(rows[1])
    return lunchA, lunchB

def _pick_snack(db: Session, goal: str, diet: str) -> dict | None:
    rows = (
        db.query(MealLibrary)
        .filter(
            MealLibrary.category == "snack",
            MealLibrary.diet_type == diet,
            MealLibrary.goal_flags.contains([goal]),
        )
        .all()
    )
    return _meal_to_json(rows[0]) if rows else None


def _pick_dinners_week(db: Session, goal: str, diet: str, fav: str | None = None) -> List[dict]:
    fav = (fav or "").strip().lower()

    if fav:
        fav_dinners = (
            db.query(MealLibrary)
            .filter(
                MealLibrary.category == "dinner",
                MealLibrary.diet_type == diet,
                MealLibrary.goal_flags.contains([goal]),
            )
            .all()
        )
        if fav_dinners:
            out = []
            total = len(fav_dinners)
            for i in range(7):
                out.append(_meal_to_json(fav_dinners[i % total]))
            return out
    dinners = (
        db.query(MealLibrary)
        .filter(
            MealLibrary.category == "dinner",
            MealLibrary.diet_type == diet,
            MealLibrary.goal_flags.contains([goal])
        )
        .all()
    )
    if not dinners:
        return [{} for _ in range(7)]

    out = []
    total = len(dinners)
    for i in range(7):
        out.append(_meal_to_json(dinners[i % total]))

    return out

def _meal_to_json(m: MealLibrary) -> dict:
    return {
        "name": m.name,
        "category": m.category,
        "ingredients": m.ingredients or [],
        "instructions": m.instructions or "",
        "macros": m.macros or {},
        "tags": m.tags or [],
    }

def build_week_meals(db: Session, goal: str | None, diet_type: str | None, fav_protein: str | None = None):
    """
    Returns structure:
    {
        mon: [ {label, meal}, ... ],
        tue: [...],
        ...
    }
    """
    g = _normalize_goal(goal)
    d = _normalize_diet(diet_type)
    fav = (fav_protein or "").strip().lower()   


    breakfast = _pick_breakfast(db, g, d, fav)
    lunchA, lunchB = _pick_lunch(db, g, d, fav) 
    snack = _pick_snack(db, g, d)
    dinners_7 = _pick_dinners_week(db, g, d, fav)

    if not (breakfast and lunchA and snack):
        return {k: [] for k in DOW}

    week: Dict[str, List[Dict]] = {}
    for i, dow in enumerate(DOW):
        lunch_for_day = lunchA if i < 3 else lunchB

        week[dow] = [
            {"label": "Breakfast", "meal": breakfast},
            {"label": "Lunch", "meal": lunch_for_day},
            {"label": "Snack", "meal": snack},
            {"label": "Dinner", "meal": dinners_7[i]},
        ]
    return week


def build_grocery_list(week_meals: Dict[str, List[Dict]]) -> List[str]:
    items = set()

    for day in week_meals.values():
        for entry in day:
            meal = entry.get("meal", {})
            for ing in meal.get("ingredients", []):
                items.add(ing.lower())

    return sorted(items)
