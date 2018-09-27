from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def dash():
    return render_template("dash.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/signup')
def signup():
    return render_template("signup.html")
