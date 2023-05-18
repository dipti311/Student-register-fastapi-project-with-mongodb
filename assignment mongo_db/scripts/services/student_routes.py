from fastapi import APIRouter
from scripts.schemas import models
from scripts.schemas.models import email
from scripts.core.handlers.st_handler import student_routes_obj
student=APIRouter()
@student.get("/all")
def show_all():
    return student_routes_obj.get_all()
@student.post("/create")
def register(data:models.Student):
    return student_routes_obj.create(data)
@student.get("/get-name")
def get_by_name(name:str):
    return student_routes_obj.get_one(name)
@student.delete("/delete")
def delete_student(name:str):
    return student_routes_obj.delete(name)
@student.put("/update")
def update_student(data:models.Student,name:str):
    return student_routes_obj.update(data,name)
@student.post("/send_email")
def send_email_student(Email: email):
    return student_routes_obj.send_email(Email)
