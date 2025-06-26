from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import date

app = FastAPI()

# --------------------- MODELS ---------------------

class Student(BaseModel):
    id: int
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    age: int
    city: str

class ClassInfo(BaseModel):
    id: int
    class_name: str
    description: str
    start_date: date
    end_date: date
    hours: int

# --------------------- DATABASES (IN-MEMORY) ---------------------

students: Dict[int, Student] = {}
classes: Dict[int, ClassInfo] = {}
registrations: Dict[int, List[int]] = {} # class_id -> list of student_ids

# --------------------- STUDENT ENDPOINTS ---------------------

@app.post("/students/")
def create_student(student: Student):
    if student.id in students:
        raise HTTPException(status_code=400, detail="Student already exists")
    students[student.id] = student
    return student

@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    students[student_id] = student
    return student

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    del students[student_id]
    return {"message": "Student deleted"}

# --------------------- CLASS ENDPOINTS ---------------------

@app.post("/classes/")
def create_class(class_info: ClassInfo):
    if class_info.id in classes:
        raise HTTPException(status_code=400, detail="Class already exists")
    classes[class_info.id] = class_info
    registrations[class_info.id] = []
    return class_info

@app.put("/classes/{class_id}")
def update_class(class_id: int, class_info: ClassInfo):
    if class_id not in classes:
        raise HTTPException(status_code=404, detail="Class not found")
    classes[class_id] = class_info
    return class_info

@app.delete("/classes/{class_id}")
def delete_class(class_id: int):
    if class_id not in classes:
        raise HTTPException(status_code=404, detail="Class not found")
    del classes[class_id]
    del registrations[class_id]
    return {"message": "Class deleted"}

# --------------------- REGISTRATION ENDPOINTS ---------------------

@app.post("/register/")
def register_student(class_id: int, student_id: int):
    if class_id not in classes or student_id not in students:
        raise HTTPException(status_code=404, detail="Class or Student not found")
    registrations[class_id].append(student_id)
    return {"message": f"Student {student_id} registered to class {class_id}"}

@app.get("/classes/{class_id}/students")
def get_registered_students(class_id: int):
    if class_id not in registrations:
        raise HTTPException(status_code=404, detail="Class not found")
    return [students[sid] for sid in registrations[class_id]]