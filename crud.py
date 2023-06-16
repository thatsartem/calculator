from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy import func, select, desc

import schemas
import models

def get_directions_by_university(db: Session, subjects: schemas.OptionsUniversities):
    if subjects.forms:
        return db.query(models.Directions).filter(
            models.Directions.subjects.contains(subjects.subjects),
            models.Directions.university.like(subjects.university),
            models.Directions.form.in_(subjects.forms)
            ).all()
    else:
        return db.query(models.Directions).filter(
            models.Directions.subjects.contains(subjects.subjects),
            models.Directions.university.like(subjects.university)
            ).all()

def get_directions_by_subjects(db: Session, subjects: schemas.OptionsUniversities):
    if subjects.forms:
        return db.query(models.Directions).filter(
            models.Directions.subjects.contains(subjects.subjects),
            models.Directions.form.in_(subjects.forms)
            ).all()
    else:
        return db.query(models.Directions).filter(
            models.Directions.subjects.contains(subjects.subjects)
            ).all()

def get_universities_by_subjects(db: Session, subjects: schemas.OptionsUniversities):
    q = db.query(
        models.Directions.university.label("name"),
        func.count(models.Directions.id).label("count"),
        func.avg(models.Directions.tuition_fee).label('avg_tuition_fee'),
        func.avg(models.Directions.passing_score).label('avg_passing_score'))\
        .filter(models.Directions.subjects.contains(subjects.subjects))
    if subjects.forms:
        universities = q.filter(models.Directions.form.in_(subjects.forms)).group_by(models.Directions.university)\
                .order_by(desc("count")).all()
    else:
        universities = q.group_by(models.Directions.university)\
                .order_by(desc("count")).all()
    return universities