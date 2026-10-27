from pydantic import BaseModel
from typing import Optional, List

class AttendanceCreate(BaseModel):
    student_id: str
    date: str
    status: str  # 'Present' or 'Absent'

class MarkCreate(BaseModel):
    student_id: str
    semester: int
    subject: str
    marks_obtained: float
    max_marks: float
    marksheet_url: Optional[str] = None

class FeeUpdate(BaseModel):
    student_id: str
    amount_paid: float
    payment_date: str
