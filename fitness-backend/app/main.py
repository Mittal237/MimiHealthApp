from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import Base, engine
from app.router import plan, auth  

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fitness Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)  
app.include_router(plan.router)

@app.get("/")
def root():
    return {"status": "ok", "service": "fitness-backend"}

@app.get("/health")
def health():
    return {"ok": True}
