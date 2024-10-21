from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    number_cats = int(request.form.get("cat_number"))
    if number_cats <= 3:
        return render_template("cat1.html")
    elif number_cats <= 6:
        return render_template("cat2.html")
    else:
        return render_template("cat3.html")
