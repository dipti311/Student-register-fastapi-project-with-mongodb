from fastapi import FastAPI
app = FastAPI()

import smtplib
from pydantic import  BaseModel
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class email(BaseModel):
    rec_email: str
    subject: str
    body: str
@app.post("/send_email")
def send_email(Email: email):
    # Set up the email details
    sender_email = "diptimishra.sultanpur@gmail.com"
    sender_password = "ssurfkdkaedvyzjo"
    receiver_email = Email.rec_email

    # Create a multipart message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = Email.subject
    
   # Add the body to the email
    message.attach(MIMEText(Email.body, "plain"))

    try:
        # Create a secure connection to the SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        # Login to the sender's email account
        server.login(sender_email, sender_password)
        
         # Send the email
        server.send_message(message)

        # Close the connection
        server.quit()

        return {"message": "Email sent successfully"}
    
    except Exception as e:
        return {"message": str(e)}