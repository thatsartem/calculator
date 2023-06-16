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
    passing_score: Optional[int]
    tuition_fee: int
    mean: int
    dispersion: int
    link: str
    chance: float = -1

    class Config:
        orm_mode = True

class OptionsDirections(BaseModel):
    subjects: List[int]
    university: Optional[str] = None
    forms: Optional[List[str]] = []
    formats: Optional[List[str]] = None
    achievs: Optional[List[str]] = None
    total_score: int 

class OptionsUniversities(BaseModel):
    subjects: List[int]
    forms: Optional[List[str]] = None
    formats: Optional[List[str]] = None
    achievs: Optional[List[str]] = None
    total_score: Optional[int] = None

class UniverstityOut(BaseModel):
    name: str
    count: int
    avg_tuition_fee: Optional[int]
    avg_passing_score: Optional[int]

    class Config:
        orm_mode = True