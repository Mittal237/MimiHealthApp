from __future__ import annotations
from app.db import SessionLocal
from app.models_fitness import (
    ProgramTemplate,
    ProgramDayTemplate,
    ProgramWeekTemplate,
    WarmupBlock,
    CooldownBlock,
    RestDayTemplate,
)

def upsert(session, model, where: dict, values: dict):
    cols = set(model.__table__.columns.keys())

    clean_where = {k: v for k, v in where.items() if k in cols}
    clean_values = {k: v for k, v in values.items() if k in cols}

    obj = session.query(model).filter_by(**clean_where).one_or_none()
    if obj:
        for k, v in clean_values.items():
            setattr(obj, k, v)
    else:
        obj = model(**{**clean_where, **clean_values})
        session.add(obj)
    return obj

def run():
    s = SessionLocal()

    upsert(
        s,
        WarmupBlock,
        {"slug": "wu_lower"},
        {
            "name": "Lower Body Warm-up",
            "duration_min": 8,
            "content": {
                "title": "Lower Body Warm-up (≈8 min)",
                "steps": [
                    {"name": "Treadmill walk or easy bike", "time_sec": 180},
                    {"name": "Bodyweight squats", "reps": 15},
                    {"name": "Leg swings (front/side)", "reps": "10/leg"},
                    {"name": "Hip circles + ankle rolls", "time_sec": 60},
                ],
            },
        },
    )

    upsert(
        s,
        WarmupBlock,
        {"slug": "wu_upper"},
        {
            "name": "Upper Body Warm-up",
            "duration_min": 8,
            "content": {
                "title": "Upper Body Warm-up (≈8 min)",
                "steps": [
                    {"name": "Arm circles (fwd/back)", "reps": "20 each"},
                    {"name": "Band pull-aparts", "reps": 15},
                    {"name": "Push-ups or incline push-ups", "reps": 10},
                    {"name": "Light cable row", "reps": 15},
                ],
            },
        },
    )

    upsert(
        s,
        WarmupBlock,
        {"slug": "wu_core"},
        {
            "name": "Core Warm-up",
            "duration_min": 6,
            "content": {
                "title": "Core Warm-up (≈6 min)",
                "steps": [
                    {"name": "Cat–Cow", "reps": 10},
                    {"name": "Bird-dog", "reps": "10/side"},
                    {"name": "Dead bug", "reps": "10/side"},
                ],
            },
        },
    )

    upsert(
        s,
        CooldownBlock,
        {"slug": "cd_lower"},
        {
            "name": "Lower Body Cool-down",
            "duration_min": 6,
            "content": {
                "title": "Lower Body Cool-down (5–6 min)",
                "steps": [
                    {"name": "Easy walk/bike", "time_sec": 120},
                    {"name": "Quad stretch", "time_sec": 30, "side": "each"},
                    {"name": "Hamstring stretch", "time_sec": 30, "side": "each"},
                    {"name": "Seated/lying glute stretch", "time_sec": 30, "side": "each"},
                    {"name": "Breathing (box 4–4–4–4)", "time_sec": 60},
                ],
            },
        },
    )

    upsert(
        s,
        CooldownBlock,
        {"slug": "cd_upper"},
        {
            "name": "Upper Body Cool-down",
            "duration_min": 6,
            "content": {
                "title": "Upper Body Cool-down (5–6 min)",
                "steps": [
                    {"name": "Doorway chest stretch", "time_sec": 30},
                    {"name": "Lat stretch (bar/pole)", "time_sec": 30, "side": "each"},
                    {"name": "Triceps stretch", "time_sec": 30, "side": "each"},
                    {"name": "Neck rolls + deep breathing", "time_sec": 60},
                ],
            },
        },
    )

    upsert(
        s,
        CooldownBlock,
        {"slug": "cd_core"},
        {
            "name": "Core Cool-down",
            "duration_min": 6,
            "content": {
                "title": "Core Cool-down (5–6 min)",
                "steps": [
                    {"name": "Child’s Pose", "time_sec": 30},
                    {"name": "Cobra stretch", "time_sec": 30},
                    {"name": "Supine twist", "time_sec": 30, "side": "each"},
                    {"name": "Box breathing", "time_sec": 60},
                ],
            },
        },
    )

    upsert(
        s,
        RestDayTemplate,
        {"slug": "rest_active_recovery"},
        {
            "name": "Active Recovery Day",
            "duration_min": 30,
            "content": {
                "title": "Active Recovery (≈30 min)",
                "steps": [
                    {"name": "Brisk walk or easy bike", "time_sec": 1200},  # 20 min
                    {"name": "Foam roll or light yoga", "time_sec": 600},   # 10 min
                ],
            },
        },
    )

    s.flush()

    wu_by_slug = {w.slug: w.id for w in s.query(WarmupBlock).all()}
    cd_by_slug = {c.slug: c.id for c in s.query(CooldownBlock).all()}
    rest_by_slug = {r.slug: r.id for r in s.query(RestDayTemplate).all()}

    prog = upsert(
        s,
        ProgramTemplate,
        {"slug": "muscle_gain_beginner"},
        {
            "name": "Muscle Gain – Beginner (5 days + 2 rest)",
            "goal": "muscle_gain",
            "level": "beginner",
            "days_per_week": 5,
            "duration_weeks": 4,
            "is_active": True,
            "note": "Pattern: train, train, rest, train, train, train, rest.",
        },
    )

    s.flush()
    prog = s.query(ProgramTemplate).filter_by(slug="muscle_gain_beginner").one()
    prog_id = prog.id

    day_defs = [
        (1, "Legs A",    "wu_lower", "cd_lower"),
        (2, "Pull A",    "wu_upper", "cd_upper"),
        # day 3 is rest
        (4, "Lower Vol", "wu_lower", "cd_lower"),
        (5, "Push A",    "wu_upper", "cd_upper"),
        (6, "Core",      "wu_core",  "cd_core"),
        # day 7 is rest
    ]
    for day_number, name, wu_slug, cd_slug in day_defs:
        upsert(
            s,
            ProgramDayTemplate,
            {"program_id": prog_id, "day_number": day_number},
            {
                "name": name,
                "focus": "",
                "warmup_block_id": wu_by_slug.get(wu_slug),
                "cooldown_block_id": cd_by_slug.get(cd_slug),
            },
        )

    week_map = [
        (1, 1, False, None),                       # Mon -> Legs A
        (2, 2, False, None),                       # Tue -> Pull A
        (3, None, True, "rest_active_recovery"),   # Wed -> Rest
        (4, 4, False, None),                       # Thu -> Lower Vol
        (5, 5, False, None),                       # Fri -> Push A
        (6, 6, False, None),                       # Sat -> Core
        (7, None, True, "rest_active_recovery"),   # Sun -> Rest
    ]
    for weekday, day_number, is_rest, rest_slug in week_map:
        upsert(
            s,
            ProgramWeekTemplate,
            {"program_id": prog_id, "weekday": weekday},
            {
                "day_number": day_number,
                "is_rest": is_rest,
                "rest_day_id": rest_by_slug.get(rest_slug) if rest_slug else None,
            },
        )

    prog_fl = upsert(
        s,
        ProgramTemplate,
        {"slug": "fat_loss_beginner"},
        {
            "name": "Fat Loss – Beginner (5 days + 2 rest)",
            "goal": "fat_loss",
            "level": "beginner",
            "days_per_week": 5,
            "duration_weeks": 4,
            "is_active": True,
            "note": "Pattern: train, train, rest, train, train, train, rest.",
        },
    )

    s.flush()
    prog_fl = s.query(ProgramTemplate).filter_by(slug="fat_loss_beginner").one()
    prog_fl_id = prog_fl.id

    fl_day_defs = [
        (1, "Full Body A (Strength + Cardio Finisher)", "wu_lower", "cd_lower"),
        (2, "Upper (Push + Pull) + Finisher",            "wu_upper", "cd_upper"),
        # day 3 is rest
        (4, "Lower + Core (Fat-Loss)",                   "wu_lower", "cd_lower"),
        (5, "Conditioning + Mobility (Active Fat Burn)", "wu_upper", "cd_upper"),
        (6, "Light Core & Recovery (Active Fat Burn)",   "wu_core",  "cd_core"),
        # day 7 is rest
    ]
    for day_number, name, wu_slug, cd_slug in fl_day_defs:
        upsert(
            s,
            ProgramDayTemplate,
            {"program_id": prog_fl_id, "day_number": day_number},
            {
                "name": name,
                "focus": "",
                "warmup_block_id": wu_by_slug.get(wu_slug),
                "cooldown_block_id": cd_by_slug.get(cd_slug),
            },
        )

    fl_week_map = [
        (1, 1, False, None),                       # Mon -> Full Body A (Strength + Cardio Finisher)
        (2, 2, False, None),                       # Tue -> Upper (Push + Pull) + Finisher
        (3, None, True, "rest_active_recovery"),   # Wed -> Rest
        (4, 4, False, None),                       # Thu -> Lower + Core (Fat-Loss)
        (5, 5, False, None),                       # Fri -> Conditioning + Mobility (Active Fat Burn)
        (6, 6, False, None),                       # Sat -> Light Core & Recovery (Active Fat Burn)
        (7, None, True, "rest_active_recovery"),   # Sun -> Rest
    ]
    for weekday, day_number, is_rest, rest_slug in fl_week_map:
        upsert(
            s,
            ProgramWeekTemplate,
            {"program_id": prog_fl_id, "weekday": weekday},
            {
                "day_number": day_number,
                "is_rest": is_rest,
                "rest_day_id": rest_by_slug.get(rest_slug) if rest_slug else None,
            },
        )

    s.commit()
    s.close()
    print("Seeded: warm-ups, cool-downs, rest day, and programs for muscle_gain_beginner & fat_loss_beginner (with week maps).")


if __name__ == "__main__":
    run()
