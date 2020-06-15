from flask import Flask, render_template, request, session, logging, url_for, redirect, flash
from passlib.hash import sha256_crypt
from pymongo import MongoClient
#working on database
cluster = MongoClient("mongodb+srv://tanpopo:crazyKuraishi@ayaka-g5z92.mongodb.net/kagari?retryWrites=true&w=majority")

#getting database
db = cluster.get_database('kagari')

#collection object
table = db.fakebook


app = Flask(__name__, instance_relative_config=True)
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        person = request.form.get("user")
        key = request.form.get("pass")
        sample = table.find_one({"username": person})
        if sample:
            if sha256_crypt.verify(key, sample["password"]):
                #session
                session["log"] = True
                gmail = str(sample["mail"])
                #home page or you can say profile page of the user
                return render_template('home.html', name=person, val=gmail)
            else:
                flash("incorrect password", "danger")
                return render_template('login.html')
        else:
            flash("user not found", "danger")
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        user = request.form.get("username")
        x = table.find_one({'username': user})
        if x:
            flash("user already exists", "info")
            return render_template("register.html")
        else:
            mail = request.form.get("mail")
            password = request.form.get("password")
            confirm = request.form.get("confirm")
            if password != confirm:
                flash("password didn't match", "danger")
                return render_template("register.html")
            else:
                incrypt_password = sha256_crypt.encrypt(str(password))
                dictonary = {
                    'username': user,
                    'mail': mail,
                    'password': incrypt_password
                }
                table.insert_one(dictonary)
                return redirect(url_for('login'))

    else:
        return render_template("register.html")

@app.route('/logout')
def profile():
    session.clear()
    flash("You are logged out", "info")
    return render_template("index.html")

if __name__ == "__main__":
    app.secret_key="whydoWeNeedSecret_key123"
    app.run(debug=True)