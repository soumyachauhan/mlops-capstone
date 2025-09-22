import time
import smtplib
from email.message import EmailMessage
import os 
from dotenv import load_dotenv
load_dotenv()

LOG_FILE = "predictions.log"
THRESHOLD = 0.2  # 20% error rate
CHECK_INTERVAL = 10  # seconds

def send_email_alert(subject, body):
    # Configure your email
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    
    msg = EmailMessage()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS  
    msg['Subject'] = subject
    msg.set_content(body)
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

def monitor_logs():
    while True:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
        
        if not lines:
            time.sleep(CHECK_INTERVAL)
            continue

        errors = [line for line in lines if "ERROR" in line]
        error_rate = len(errors) / len(lines)

        if error_rate > THRESHOLD:
            send_email_alert(
                "ML App Alert: High Error Rate",
                f"Error rate is {error_rate*100:.2f}%!\nCheck the log file."
            )
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_logs()