from __future__ import annotations
from typing import Literal, Dict

Activity = Literal["Sedentary", "Light", "Moderate", "Intense"]
Goal     = Literal["Lose Fat", "Build Muscle", "Maintain"]

ACTIVITY_MULT = {
    "Sedentary": 1.2,
    "Light":     1.375,
    "Moderate":  1.55,
    "Intense":   1.725,
}

def cm_to_m(cm: float | None) -> float | None:
    return None if cm is None else (cm / 100.0)

def mifflin_st_jeor(sex: str | None, age: int | None, height_cm: float | None, weight_kg: float | None) -> float:
    """
    BMR (kcal/day) — Mifflin-St Jeor.
    Uses 'Male'/'Female' if provided; defaults to male constant if unknown.
    """
    if not all([age, height_cm, weight_kg]):
        # fallback conservative BMR if data incomplete
        return 1700.0

    s = 5 if (sex or "").lower().startswith("m") else -161
    return 10 * weight_kg + 6.25 * height_cm - 5 * age + s

def tdee(bmr: float, activity: Activity | str | None) -> float:
    mult = ACTIVITY_MULT.get(str(activity or "Light"), 1.375)
    return bmr * mult

def macro_targets(tdee_cal: float, goal: Goal | str | None, weight_kg: float | None) -> Dict[str, int]:
    """
    Returns rounded integer targets: calories, protein_g, carbs_g, fat_g.
    Heuristics:
      - Lose Fat:   15–20% deficit, protein 2.0–2.2 g/kg
      - Build Musc: 5–10% surplus,  protein 1.8–2.2 g/kg
      - Maintain:   ±0%,            protein 1.6–2.0 g/kg
    Carbs/fats split after protein: default ~45/30 (can be tuned per goal).
    """
    g = (goal or "Maintain")
    if g == "Lose Fat":
        calories = int(round(tdee_cal * 0.85))
        prot_per_kg = 2.1
        carb_share, fat_share = 0.45, 0.30
    elif g == "Build Muscle":
        calories = int(round(tdee_cal * 1.07))
        prot_per_kg = 2.0
        carb_share, fat_share = 0.50, 0.25
    else:
        calories = int(round(tdee_cal))
        prot_per_kg = 1.8
        carb_share, fat_share = 0.50, 0.25

    protein_g = int(round((weight_kg or 70) * prot_per_kg))

    rem_kcal = max(calories - protein_g * 4, int(calories * 0.4))

    carbs_kcal = int(rem_kcal * carb_share)
    fat_kcal   = int(rem_kcal * fat_share)

    carbs_g = int(round(carbs_kcal / 4))
    fat_g   = int(round(fat_kcal / 9))

    return {
        "calorieTarget": calories,
        "proteinTarget": protein_g,
        "carbsTarget":   carbs_g,
        "fatTarget":     fat_g,
    }

def compute_daily_targets(
    sex: str | None,
    age: int | None,
    height_cm: float | None,
    weight_kg: float | None,
    activity: Activity | str | None,
    goal: Goal | str | None,
) -> Dict[str, int]:
    b = mifflin_st_jeor(sex, age, height_cm, weight_kg)
    td = tdee(b, activity)
    return macro_targets(td, goal, weight_kg)
