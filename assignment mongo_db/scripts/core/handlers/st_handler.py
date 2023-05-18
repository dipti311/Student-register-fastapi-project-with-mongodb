
from scripts.utils import db
from scripts.utils.db import collection
from scripts.schemas import models
from scripts.schemas.models import email 
import smtplib
from scripts.core.handlers.aggre import result
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
class Student_Routes:
    def get_all(self):
        data=db.all()
        return{"data":data}

    def create(self,data:models.Student):
        id=db.create(data)
        return {"inserted":True,"inserted_id":id}

    def get_one(self,name:str):
        data=db.get_one(name)
        return {"data":data}

    def delete(self,name:str):
        data=db.delete(name)
        return {"deleted":True,"deleted_count":data}

    def update(self,data:models.Student,name:str):
        print(name)
        data=db.update(data,name=name)
        return {"updated":True,"updated_count":data}
    def aggregate(self):
        agg=collection.aggregate(result)
        agg_list=list(agg)
        return agg_list[0]["course_fee"]

    def send_email(self,Email: email):
        sender_email = "diptimishra.sultanpur@gmail.com"
        sender_password = "ssurfkdkaedvyzjo"
        receiver_email = Email.rec_email
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = Email.subject
        body=self.aggregate()
        body=str(body)
        message.attach(MIMEText("total cost of course fee is "+body, "plain"))
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
            server.quit()
            return {"message": "Email sent successfully"}
    
        except Exception as e:
            return {"message": str(e)}
    
student_routes_obj=Student_Routes()