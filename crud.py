from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy import func, select, desc


import models

def get_directions_by_university(db: Session, subjects, university):
    return db.query(models.Directions).filter(models.Directions.subjects.contains(subjects))\
        .filter(models.Directions.university==university).all()

def get_directions_by_subjects(db: Session, subjects):
    return db.query(models.Directions).filter(models.Directions.subjects.contains(subjects)).all()

def get_universities_by_subjects(db: Session, subjects):
    return db.query(models.Directions.university,func.count(models.Directions.id))\
        .filter(models.Directions.subjects.contains(subjects)).group_by(models.Directions.university)