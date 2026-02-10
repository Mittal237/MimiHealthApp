from __future__ import annotations

def compute_daily_targets(
    sex: str,
    age: int,
    height_cm: float,
    weight_kg: float,
    activity: str,
    goal: str,
) -> dict:
    """
    Returns a dict:
    {
        'calorieTarget': int,
        'proteinTarget': int,
        'carbsTarget': int,
        'fatTarget': int
    }
    """

    sex = (sex or "").strip().lower()
    goal = (goal or "").strip().lower()
    activity = (activity or "").strip().lower()

    if sex in {"male", "m"}:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:  
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    if activity == "sedentary":
        multiplier = 1.2
    elif activity == "light":
        multiplier = 1.375
    elif activity == "moderate":
        multiplier = 1.55
    elif activity == "intense":
        multiplier = 1.75
    else:
        multiplier = 1.375  

    tdee = bmr * multiplier

    if goal in {"build muscle", "muscle_gain", "bulk"}:
        calories = tdee + 350  # lean surplus
    elif goal in {"lose fat", "fat_loss", "cut"}:
        calories = tdee - 300
    elif goal in {"performance", "athletic"}:
        calories = tdee + 150
    else:
        calories = tdee 

    calories = int(round(calories))

    if goal in {"build muscle", "muscle_gain"}:
        protein_g = int(round(1.7 * weight_kg))
    elif goal in {"lose fat", "fat_loss"}:
        protein_g = int(round(1.9 * weight_kg))  
    else:
        protein_g = int(round(1.5 * weight_kg))

    # Fat = ~25% of calories
    fat_g = int(round((0.25 * calories) / 9))

    # Carbs = rest of calories
    carbs_kcal = calories - (protein_g * 4 + fat_g * 9)
    carbs_g = max(0, int(round(carbs_kcal / 4)))

    return {
        "calorieTarget": calories,
        "proteinTarget": protein_g,
        "carbsTarget": carbs_g,
        "fatTarget": fat_g,
    }
