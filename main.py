import os
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

# Authentication dependency with default "test" fallback for local/Swagger testing
async def verify_supabase_token(authorization: str = Header(default="test")):
    print(f"--- DEBUG: Authorization header received: {authorization} ---")
    if authorization == "test":
        return {"sub": "local-test-user"}
    # Standard token validation can go here if needed
    return {"sub": authorization}

# Pydantic model for attendance input validation
class AttendanceCreate(BaseModel):
    student_id: str
    date: str
    status: str

@app.post("/api/attendance")
async def mark_attendance(attendance: AttendanceCreate, user = Depends(verify_supabase_token)):
    print(f"--- DEBUG: POST /api/attendance called with {attendance.dict()} ---")
    try:
        response = supabase.table("attendance_records").insert(attendance.dict()).execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        print(f"--- DEBUG ERROR in mark_attendance: {str(e)} ---")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/student/{student_id}")
async def get_student_dashboard(student_id: str, user = Depends(verify_supabase_token)):
    print(f"--- DEBUG: GET /api/student/{student_id} called ---")
    try:
        # Corrected to query using 'student_id' instead of 'id'
        student_res = supabase.table("students").select("*").eq("student_id", student_id).execute()
        attendance_res = supabase.table("attendance_records").select("*").eq("student_id", student_id).execute()
        
        return {
            "student": student_res.data,
            "attendance": attendance_res.data
        }
    except Exception as e:
        print(f"--- DEBUG ERROR in student dashboard: {str(e)} ---")
        raise HTTPException(status_code=500, detail=str(e))