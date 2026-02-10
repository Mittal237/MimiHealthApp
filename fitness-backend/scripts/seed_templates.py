# LEGACY NOTICE:
# This script seeds the old `workout_templates` and `meal_templates` tables.
# It is no longer used by the app. The active seeder is `app/seed_fitness.py`.
# DO NOT RUN THIS FILE — running it may overwrite or conflict with new data.
# /Applications/fitness-backend/scripts/seed_templates.py
from app.db import session_scope
from app.models import WorkoutTemplate, MealTemplate

def upsert_workout(goal, day_type, focus, details, coach_note, difficulty="beginner", duration_min=45, equipment=None):
    equipment = equipment or []
    with session_scope() as db:
        wt = db.query(WorkoutTemplate).filter_by(goal=goal, day_type=day_type).one_or_none()
        if wt is None:
            wt = WorkoutTemplate(
                goal=goal,
                day_type=day_type,
                focus=focus,
                details=details,
                coach_note=coach_note,
                difficulty=difficulty,
                duration_min=duration_min,
                equipment=equipment,
            )
            db.add(wt)
        else:
            wt.focus = focus
            wt.details = details
            wt.coach_note = coach_note
            wt.difficulty = difficulty
            wt.duration_min = duration_min
            wt.equipment = equipment

def upsert_meal(goal, diet_type, day_index, meals_for_day, prep_time_min=15, tags=None):
    tags = tags or []
    with session_scope() as db:
        mt = db.query(MealTemplate).filter_by(goal=goal, diet_type=diet_type, day_index=day_index).one_or_none()
        if mt is None:
            mt = MealTemplate(
                goal=goal,
                diet_type=diet_type,
                day_index=day_index,
                meals_for_day=meals_for_day,
                prep_time_min=prep_time_min,
                tags=tags,
            )
            db.add(mt)
        else:
            mt.meals_for_day = meals_for_day
            mt.prep_time_min = prep_time_min
            mt.tags = tags

def main():
    # Example: Build Muscle workouts
    upsert_workout("muscle_gain", "Push A", "Push (Chest/Shoulders/Triceps)",
                   ["DB Bench Press 4x8-10", "Shoulder Press 3x10", "Fly 3x12-15", "Tricep Pushdown 3x12-15"],
                   "Last 2 reps slow and controlled.", difficulty="intermediate")
    upsert_workout("muscle_gain", "Pull A", "Pull (Back/Biceps)",
                   ["1-arm Row 4x10/side", "Lat Pulldown 4x8-10", "Face Pull 3x15", "Curl 3x12-15"],
                   "Pull with elbows, not hands.", difficulty="intermediate")
    upsert_workout("muscle_gain", "Legs A", "Legs (Glutes/Quads/Hamstrings)",
                   ["Back Squat 4x8-10", "RDL 3x10", "Walking Lunge 3x12/leg", "Leg Press 3x12"],
                   "Control the negative.", difficulty="intermediate")
    upsert_workout("muscle_gain", "Rest", "Rest", [], "Rest up.", difficulty="beginner", duration_min=0)

    # 7-day meal templates (non-veg)
    nonveg_meals = [
        {"label": "Breakfast", "text": "Eggs + oats + banana"},
        {"label": "Lunch", "text": "Chicken rice bowl + veggies"},
        {"label": "Dinner", "text": "Salmon + potatoes + greens"},
        {"label": "Snack", "text": "Whey shake + fruit"},
    ]
    for d in range(7):
        upsert_meal("Build Muscle", "nonveg", d, nonveg_meals)

    # 7-day meal templates (veg)
    veg_meals = [
        {"label": "Breakfast", "text": "Greek yogurt + granola + berries"},
        {"label": "Lunch", "text": "Paneer rice bowl + veggies"},
        {"label": "Dinner", "text": "Tofu stir-fry + rice"},
        {"label": "Snack", "text": "Protein smoothie"},
    ]
    for d in range(7):
        upsert_meal("Build Muscle", "veg", d, veg_meals)

    print("✅ Seeded workout_templates and meal_templates")

if __name__ == "__main__":
    main()
