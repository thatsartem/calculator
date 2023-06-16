from typing import List
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

import schemas
import models
import crud
from database import SessionLocal, engine
from formulas import get_percentage

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/get_directions/", response_model=List[schemas.Direction])
def get_directions(subjects: schemas.OptionsDirections, db: Session = Depends(get_db)):
    if not subjects.university:
        directions = crud.get_directions_by_subjects(db, subjects)
    else:
        directions = crud.get_directions_by_university(db, subjects)
    for d in directions:
        if d.mean != -1 and d.dispersion != -1:
            d.chance = get_percentage(subjects.total_score,d.mean,d.dispersion)
    return directions

@app.post("/api/get_universities/", response_model=List[schemas.UniverstityOut])
def get_universities(subjects: schemas.OptionsUniversities, db: Session = Depends(get_db)):
    universities = crud.get_universities_by_subjects(db, subjects)
    return universities

@app.get("/")
def ping():
    return {"ping": "pong"}
