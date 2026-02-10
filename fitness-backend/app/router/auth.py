# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
import bcrypt

from app.db import get_db
from app.models import User, UserProfile
from fastapi import Query

router = APIRouter(prefix="/auth", tags=["auth"])

# ----- Schemas
class SignupReq(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class ProfileReq(BaseModel):
    user_id: str
    age: int | None = None
    sex: str | None = None
    height_cm: float | None = None
    weight_kg: float | None = None
    activity_level: str | None = None
    goal: str | None = None
    diet_type: str | None = None
    fav_protein: str | None = None
    experience_level: str | None = None

@router.post("/signup")
def signup(req: SignupReq, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.email == req.email).one_or_none()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    pwd_hash = bcrypt.hashpw(req.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    user = User(
        first_name=req.first_name,
        last_name=req.last_name,
        email=req.email,
        password_hash=pwd_hash,
    )
    db.add(user)
    db.flush()  # get user.id

    # create empty profile row (optional, but convenient)
    profile = UserProfile(user_id=user.id)
    db.add(profile)
    db.commit()

    return {"userId": str(user.id)}

@router.post("/profile/setup")
def save_profile(req: ProfileReq, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == req.user_id).one_or_none()
    if not profile:
        # create if missing
        profile = UserProfile(user_id=req.user_id)
        db.add(profile)
        db.flush()

    # update fields
    profile.age = req.age
    profile.sex = req.sex
    profile.height_cm = req.height_cm
    profile.weight_kg = req.weight_kg
    profile.activity_level = req.activity_level
    profile.goal = req.goal
    profile.diet_type = req.diet_type
    profile.fav_protein = req.fav_protein
    profile.experience_level = req.experience_level

    db.commit()
    return {"ok": True}

# --- READ-ONLY: get existing user profile ---
@router.get("/profile")
def get_profile(user_id: str = Query(..., description="User ID"),
                db: Session = Depends(get_db)):
    """Return stored profile for debugging."""
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return {
        "user_id": profile.user_id,
        "goal": profile.goal,
        "activity_level": profile.activity_level,
        "diet_type": profile.diet_type,
        "height_cm": profile.height_cm,
        "weight_kg": profile.weight_kg,
        "sex": profile.sex,
        "fav_protein": profile.fav_protein,
        "experience_level": profile.experience_level,
    }

