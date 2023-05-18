from pydantic import BaseModel
class Student(BaseModel):
    name: str
    roll_no:int
    course_name:str
    course_fee:int
class email(BaseModel):
    rec_email: str
    subject: str
