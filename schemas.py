from typing import List, Optional
from pydantic import BaseModel

class Direction(BaseModel):
    id: int
    name: str
    university: str
    code: str
    form: str
    subjects: List[int]
    budget_seats: int
    paid_seats: int
    passing_score: int
    tuition_fee: int
    mean: int
    dispersion: int

    class Config:
        orm_mode = True

class SubjectsIn(BaseModel):
    subjects: List[int]
    university: Optional[str] = None