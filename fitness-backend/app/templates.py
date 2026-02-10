MEAL_TEMPLATES = {
  
    ("muscle_gain", "nonveg"): {
        0: [
            {"label": "Breakfast", "text": "Eggs + oats + peanut butter + banana"},
            {"label": "Lunch", "text": "Chicken bowl with rice + veggies"},
            {"label": "Dinner", "text": "Salmon + potatoes + greens"},
            {"label": "Post-Workout", "text": "Whey shake + fruit"},
        ],
        1: [
            {"label": "Breakfast", "text": "Greek yogurt + granola + berries"},
            {"label": "Lunch", "text": "Turkey wrap + avocado + veggies"},
            {"label": "Dinner", "text": "Lean beef + rice + veggies"},
            {"label": "Snack", "text": "Cottage cheese + pineapple"},
        ],
        2: [
            {"label": "Breakfast", "text": "Omelet (egg whites + veg) + toast"},
            {"label": "Lunch", "text": "Grilled chicken salad (olive oil)"},
            {"label": "Dinner", "text": "Shrimp stir-fry + jasmine rice"},
            {"label": "Snack", "text": "Protein bar or whey + banana"},
        ],
        3: [
            {"label": "Breakfast", "text": "Overnight oats + chia + berries + whey"},
            {"label": "Lunch", "text": "Chicken tikka + basmati rice + cucumber"},
            {"label": "Dinner", "text": "Beef/chicken chili + potatoes"},
            {"label": "Snack", "text": "Greek yogurt + honey"},
        ],
        4: [
            {"label": "Breakfast", "text": "Egg sandwich + cheese + tomato"},
            {"label": "Lunch", "text": "Tuna wrap + spinach + avocado"},
            {"label": "Dinner", "text": "Teriyaki chicken + rice + broccoli"},
            {"label": "Snack", "text": "Milk + mixed nuts"},
        ],
        5: [
            {"label": "Breakfast", "text": "Protein pancakes + berries"},
            {"label": "Lunch", "text": "Chicken burrito bowl (beans, rice, salsa)"},
            {"label": "Dinner", "text": "Steak + sweet potato + asparagus"},
            {"label": "Snack", "text": "Cottage cheese + crackers"},
        ],
        6: [
            {"label": "Breakfast", "text": "Bagel + eggs + cream cheese"},
            {"label": "Lunch", "text": "Grilled chicken pasta + marinara"},
            {"label": "Dinner", "text": "Fish tacos + slaw"},
            {"label": "Snack", "text": "Whey + fruit"},
        ],
    },

    ("muscle_gain", "veg"): {
        0: [
            {"label": "Breakfast", "text": "Paneer scramble + roti + avocado"},
            {"label": "Lunch", "text": "Tofu + rice + veggies bowl"},
            {"label": "Dinner", "text": "Dal + quinoa + mixed veg"},
            {"label": "Post-Workout", "text": "Whey/pea shake + fruit"},
        ],
        1: [
            {"label": "Breakfast", "text": "Greek yogurt + berries + chia"},
            {"label": "Lunch", "text": "Chickpea salad + cucumber + olive oil"},
            {"label": "Dinner", "text": "Paneer tikka + roti + veg"},
            {"label": "Snack", "text": "Cottage cheese + pineapple"},
        ],
        2: [
            {"label": "Breakfast", "text": "Overnight oats + peanut butter + banana"},
            {"label": "Lunch", "text": "Veggie burrito bowl (beans, rice, salsa)"},
            {"label": "Dinner", "text": "Tofu stir-fry + noodles/rice"},
            {"label": "Snack", "text": "Pea protein shake + fruit"},
        ],
        3: [
            {"label": "Breakfast", "text": "Moong dal chilla + yogurt"},
            {"label": "Lunch", "text": "Paneer rice bowl + veggies"},
            {"label": "Dinner", "text": "Chole + jeera rice + salad"},
            {"label": "Snack", "text": "Milk + dry fruits"},
        ],
        4: [
            {"label": "Breakfast", "text": "Upma + peanuts + yogurt"},
            {"label": "Lunch", "text": "Tofu wrap + avocado + veggies"},
            {"label": "Dinner", "text": "Veg korma + paratha + salad"},
            {"label": "Snack", "text": "Greek yogurt + honey"},
        ],
        5: [
            {"label": "Breakfast", "text": "Protein pancakes (whey/pea) + berries"},
            {"label": "Lunch", "text": "Rajma + rice + salad"},
            {"label": "Dinner", "text": "Paneer bhurji + roti + veg"},
            {"label": "Snack", "text": "Cottage cheese + crackers"},
        ],
        6: [
            {"label": "Breakfast", "text": "Bagel + cream cheese + tofu scramble"},
            {"label": "Lunch", "text": "Hummus bowl (pita, veg, olives)"},
            {"label": "Dinner", "text": "Veg noodles + edamame"},
            {"label": "Snack", "text": "Whey/pea shake + fruit"},
        ],
    },
}

WORKOUT_TEMPLATES = [
    # --------- Legs A ---------
    {
        "goal": "muscle_gain",
        "day_type": "Legs A",
        "difficulty": "beginner",
        "focus": "Beginner Leg Day – Quads & Glutes",
        "details": [
            {"name": "Barbell Back Squat", "sets": 4, "reps": "8–10", "notes": "Chest up, neutral spine, break parallel."},
            {"name": "Romanian Deadlift (DB/Barbell)", "sets": 3, "reps": "10–12", "notes": "Hinge at hips; feel hamstring stretch."},
            {"name": "Reverse Lunge (DB/Barbell)", "sets": 3, "reps": "10/leg", "notes": "Step back to reduce knee stress."},
            {"name": "Leg Extension (Machine)", "sets": 3, "reps": "12–15", "notes": "Squeeze at top; control lowering."},
            {"name": "Standing Calf Raise", "sets": 3, "reps": "15–20", "notes": "Pause 1s at top; slow eccentric."},
        ],
        "coachNote": "~2 RIR on compounds; dial in depth/bracing.",
    },

    # --------- Pull A ---------
    {
        "goal": "muscle_gain",
        "day_type": "Pull A",
        "difficulty": "beginner",
        "focus": "Back & Biceps (with Face Pulls)",
        "details": [
            {"name": "Lat Pulldown (Wide Grip)", "sets": 4, "reps": "10–12", "notes": "Chest up; control the negative."},
            {"name": "Seated Cable Row", "sets": 3, "reps": "10–12", "notes": "Drive elbows back; neutral spine."},
            {"name": "One-Arm Dumbbell Row", "sets": 3, "reps": "10/arm", "notes": "Pull elbow to hip; bench support."},
            {"name": "Face Pull (Rope)", "sets": 3, "reps": "15–20", "notes": "Pull to face; thumbs back; arms parallel."},
            {"name": "Incline Dumbbell Curl", "sets": 3, "reps": "10–12", "notes": "Elbows slightly behind body; slow eccentric."},
            {"name": "Hammer Curl", "sets": 3, "reps": "10–12", "notes": "Neutral grip; avoid swinging."},
        ],
        "coachNote": "Pinch shoulder blades; smooth reps.",
    },

    # --------- Lower Vol (Legs B) ---------
    {
        "goal": "muscle_gain",
        "day_type": "Lower Vol",
        "difficulty": "beginner",
        "focus": "Leg Day 2 – Glutes & Hamstrings",
        "details": [
            {"name": "Barbell Hip Thrust", "sets": 4, "reps": "8–10", "notes": "Drive through heels; pause 1s at top."},
            {"name": "Sumo Squat (BB/DB)", "sets": 3, "reps": "8–10", "notes": "Wide stance; knees track toes; depth focus."},
            {"name": "Bulgarian Split Squat (DB)", "sets": 3, "reps": "10/leg", "notes": "Control the lowering; front shin vertical."},
            {"name": "Glute Kickback (Cable/Machine)", "sets": 3, "reps": "12–15/leg", "notes": "Slight knee bend; drive heel back/up."},
            {"name": "Standing Calf Raise", "sets": 3, "reps": "15–20", "notes": "Full stretch at bottom; pause at top."},
        ],
        "coachNote": "Glute squeeze each rep; own the eccentric.",
    },

    # --------- Push A ---------
    {
        "goal": "muscle_gain",
        "day_type": "Push A",
        "difficulty": "beginner",
        "focus": "Chest, Shoulders & Triceps",
        "details": [
            {"name": "Barbell Bench Press", "sets": 4, "reps": "8–10", "notes": "Elbows ~45°; full ROM; tight upper back."},
            {"name": "Incline Dumbbell Press", "sets": 3, "reps": "10–12", "notes": "Bench 30–45°; control tempo."},
            {"name": "Seated Dumbbell Shoulder Press", "sets": 3, "reps": "10–12", "notes": "Neutral spine; don’t lock elbows."},
            {"name": "Cable/DB Chest Fly", "sets": 3, "reps": "12–15", "notes": "Hug motion; slow return for stretch."},
            {"name": "Lateral Raise (DB/Cable)", "sets": 3, "reps": "12–15", "notes": "Raise to shoulder height; no swing."},
            {"name": "Triceps Rope Pushdown", "sets": 3, "reps": "12–15", "notes": "Elbows fixed; spread rope at bottom."},
            {"name": "Overhead Triceps Extension", "sets": 3, "reps": "12–15", "notes": "Upper arms vertical; get a stretch."},
        ],
        "coachNote": "Scaps set; breathe and brace.",
    },

    # --------- Core ---------
    {
        "goal": "muscle_gain",
        "day_type": "Core",
        "difficulty": "beginner",
        "focus": "Core & Abs Stability",
        "details": [
            {"name": "Hanging Knee Raise / Captain’s Chair", "sets": 3, "reps": "12–15", "notes": "Curl pelvis up; control descent."},
            {"name": "Cable Pallof Press", "sets": 3, "reps": "12/side", "notes": "Hold 2s at full extension; resist rotation."},
            {"name": "Ab Wheel Rollout / Stability Ball Rollout", "sets": 3, "reps": "10–12", "notes": "Spine neutral; range as control allows."},
            {"name": "Side Plank (with Hip Dip)", "sets": 3, "time": "30s/side", "notes": "Straight line; controlled dips."},
            {"name": "Reverse Crunch", "sets": 3, "reps": "15–20", "notes": "Curl pelvis toward chest; avoid swinging."},
            {"name": "Cable Woodchopper (High→Low)", "sets": 3, "reps": "12/side", "notes": "Control both directions; pivot feet."},
            {"name": "Plank (BW/Weighted)", "sets": 3, "time": "45–60s", "notes": "Brace abs, glutes, quads; no sag."},
        ],
        "coachNote": "Optional finisher: 10–15 min incline walk or easy bike.",
    },

    # --------- Rest (True Rest) ---------
    {
        "goal": "muscle_gain",
        "day_type": "Rest",
        "difficulty": "beginner",
        "focus": "Rest Day",
        "details": [],  
        "coachNote": "Full rest. Hydrate, eat well, and sleep.",
    },
]

SPLIT_BY_GOAL = {
    "muscle_gain": ["Legs A", "Pull A", "Rest", "Lower Vol", "Push A", "Core", "Rest"],
}
