from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    input_name = request.form.get("name")
    input_favourite_num = request.form.get("favouriteNumber")
    return render_template("hello.html", name=input_name, favouriteNumber=input_favourite_num)

     