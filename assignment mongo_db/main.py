from fastapi import FastAPI
from scripts.services.student_routes import student 
app = FastAPI()
app.include_router(student)