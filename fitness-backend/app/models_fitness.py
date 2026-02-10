from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, JSON, Text,
    UniqueConstraint, CheckConstraint
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.db import Base

class ProgramTemplate(Base):
    __tablename__ = "program_template"
    id = Column(Integer, primary_key=True)
    slug = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    goal = Column(String, nullable=False)
    level = Column(String, nullable=False)
    days_per_week = Column(Integer, nullable=False)
    duration_weeks = Column(Integer, nullable=False, default=4)
    is_active = Column(Boolean, nullable=False, default=True)

    days = relationship("ProgramDayTemplate", back_populates="program", cascade="all, delete-orphan")
    week_template = relationship("ProgramWeekTemplate", back_populates="program", cascade="all, delete-orphan")

class WarmupBlock(Base):
    __tablename__ = "warmup_block"
    id = Column(Integer, primary_key=True)
    slug = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    content = Column(JSON, nullable=False)

class CooldownBlock(Base):
    __tablename__ = "cooldown_block"
    id = Column(Integer, primary_key=True)
    slug = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    content = Column(JSON, nullable=False)

class ProgramDayTemplate(Base):
    __tablename__ = "program_day_template"
    id = Column(Integer, primary_key=True)
    program_id = Column(Integer, ForeignKey("program_template.id", ondelete="CASCADE"), nullable=False)
    day_number = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    focus = Column(String)

    warmup_block_id = Column(Integer, ForeignKey("warmup_block.id"), nullable=True)
    cooldown_block_id = Column(Integer, ForeignKey("cooldown_block.id"), nullable=True)

    coach_note = Column(Text, nullable=True)
    details_json = Column(JSONB, nullable=False, default=list)

    program = relationship("ProgramTemplate", back_populates="days")
    warmup_block = relationship("WarmupBlock")
    cooldown_block = relationship("CooldownBlock")

    __table_args__ = (UniqueConstraint("program_id", "day_number", name="uq_program_daynum"),)

class RestDayTemplate(Base):
    __tablename__ = "rest_day_template"
    id = Column(Integer, primary_key=True)
    slug = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    content = Column(JSON, nullable=False)

class ProgramWeekTemplate(Base):
    __tablename__ = "program_week_template"
    id = Column(Integer, primary_key=True)
    program_id = Column(Integer, ForeignKey("program_template.id", ondelete="CASCADE"), nullable=False)
    weekday = Column(Integer, nullable=False)
    day_number = Column(Integer, nullable=True)
    is_rest = Column(Boolean, nullable=False, default=False)
    rest_slug = Column(String, nullable=True)

    program = relationship("ProgramTemplate", back_populates="week_template")

    __table_args__ = (
        UniqueConstraint("program_id", "weekday", name="uq_program_weekday"),
        CheckConstraint("weekday BETWEEN 1 AND 7", name="ck_weekday_1_7"),
    )
