from datetime import date
from sqlalchemy.orm import Session
from app.models_fitness import (
    ProgramTemplate, ProgramWeekTemplate, ProgramDayTemplate,
    WarmupBlock, CooldownBlock, RestDayTemplate
)

def get_today_blocks(db: Session, program_slug: str, on_date: date):
    """Return warmup/cooldown (or rest block) for the given date.
       Shape:
       {
         "is_rest": bool,
         "title": str | None,        # workout title if training
         "focus": str | None,        # focus string if training
         "warmup": dict | None,      # JSON content
         "cooldown": dict | None,    # JSON content
         "rest": dict | None         # JSON content when rest day
       }
    """
    weekday = on_date.isoweekday()

    prog = db.query(ProgramTemplate).filter_by(slug=program_slug).one_or_none()
    if not prog:
        return {"is_rest": False, "title": None, "focus": None,
                "warmup": None, "cooldown": None, "rest": None}

    wt = db.query(ProgramWeekTemplate).filter_by(program_id=prog.id, weekday=weekday).one_or_none()
    if not wt:
        return {"is_rest": False, "title": None, "focus": None,
                "warmup": None, "cooldown": None, "rest": None}

    if wt.is_rest:
        rest = db.query(RestDayTemplate).filter_by(slug=wt.rest_slug).one_or_none()
        return {"is_rest": True, "title": "Rest / Active Recovery", "focus": None,
                "warmup": None, "cooldown": None, "rest": (rest.content if rest else None)}

    day = db.query(ProgramDayTemplate).filter_by(program_id=prog.id, day_number=wt.day_number).one_or_none()
    if not day:
        return {"is_rest": False, "title": None, "focus": None,
                "warmup": None, "cooldown": None, "rest": None}

    warmup = db.query(WarmupBlock).get(day.warmup_block_id) if day.warmup_block_id else None
    cooldown = db.query(CooldownBlock).get(day.cooldown_block_id) if day.cooldown_block_id else None

    return {
        "is_rest": False,
        "title": day.name,
        "focus": day.focus,
        "warmup": warmup.content if warmup else None,
        "cooldown": cooldown.content if cooldown else None,
        "rest": None
    }
