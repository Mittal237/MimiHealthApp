from sqlalchemy import (
    Column, String, Integer, Float, Text, Date, DateTime, JSON,
    ForeignKey, UniqueConstraint, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from .db import Base
from sqlalchemy.dialects.postgresql import UUID, JSONB

def uuid_pk() -> str:
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=False), primary_key=True, default=uuid_pk)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    password_hash = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    profile = relationship("UserProfile", back_populates="user", uselist=False)
    plans = relationship("WeeklyPlan", back_populates="user")

class UserProfile(Base):
    __tablename__ = "user_profile"
    user_id = Column(UUID(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    age = Column(Integer)
    sex = Column(Text)
    height_cm = Column(Float)
    weight_kg = Column(Float)
    activity_level = Column(Text)   
    goal = Column(Text)             
    diet_type = Column(Text)        
    fav_protein = Column(Text)
    experience_level = Column(Text) 
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="profile")

class WorkoutTemplate(Base):
    __tablename__ = "workout_templates"
    id = Column(UUID(as_uuid=False), primary_key=True, default=uuid_pk)
    goal = Column(Text, nullable=False)
    day_type = Column(Text, nullable=False)      
    focus = Column(Text, nullable=False)
    details = Column(JSON, nullable=False)       
    coach_note = Column(Text, nullable=False)
    equipment = Column(JSON)                      
    duration_min = Column(Integer)
    difficulty = Column(Text)                  
    __table_args__ = (
        UniqueConstraint("goal", "day_type", "difficulty", name="uq_workout_goal_day"),
    )

class MealTemplate(Base):
    __tablename__ = "meal_templates"
    id = Column(UUID(as_uuid=False), primary_key=True, default=uuid_pk)
    goal = Column(Text, nullable=False)
    diet_type = Column(Text, nullable=False)      
    day_index = Column(Integer, nullable=False)   
    meals_for_day = Column(JSON, nullable=False)  
    prep_time_min = Column(Integer)
    tags = Column(JSON)
    __table_args__ = (UniqueConstraint("goal", "diet_type", "day_index", name="uq_meal_goal_diet_day"),)

class MealLibrary(Base):
    __tablename__ = "meal_library"

    id = Column(UUID(as_uuid=False), primary_key=True, default=uuid_pk)
    name = Column(Text, nullable=False)               
    category = Column(Text, nullable=False)          
    diet_type = Column(Text, nullable=False)        
    goal_flags = Column(JSONB, nullable=False)       
    ingredients = Column(JSON)                       
    instructions = Column(Text)                       
    macros = Column(JSON, nullable=False)             
    tags = Column(JSON)                               

class WeeklyPlan(Base):
    __tablename__ = "weekly_plans"
    id = Column(UUID(as_uuid=False), primary_key=True, default=uuid_pk)
    user_id = Column(UUID(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    week_start_date = Column(Date, nullable=False, index=True)
    daily_targets = Column(JSON, nullable=False)   
    week_meals = Column(JSON, nullable=False)      
    week_workouts = Column(JSON, nullable=False)   
    grocery_list = Column(JSON, nullable=False)   
    goal = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="plans")
    __table_args__ = (UniqueConstraint("user_id", "week_start_date", name="uq_user_week"),)
