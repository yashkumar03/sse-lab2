from flask import Flask, render_template, request
import re
import math

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


@app.route("/query", methods=["GET"])
def handle_query():
    q = request.args.get("q")
    if q:
        response = process_query(q)
        return response
    return ""


def process_query(abc):
    if abc == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"
    elif abc == "asteroids":
        return "Unknown"
    elif "What is" in abc and "multiplied" in abc:
        numbers = re.findall(r"\d+", abc)
        numbers = [int(num) for num in numbers]
        return str(numbers[0] * numbers[1])

    elif "What is" in abc:
        numbers = re.findall(r"\d+", abc)
        numbers = [int(num) for num in numbers]
        return str(numbers[0] + numbers[1])

    elif "Which of the following numbers is the largest" in abc:
        numbers = re.findall(r"\d+", abc)
        numbers = [int(num) for num in numbers]
        return str(max(numbers))
    # elif "Which of the following numbers is both a square and a cube" in abc:
    #     numbers = re.findall(r'\d+', abc)
    #     numbers = [int(num) for num in numbers]
    #     for number in numbers:
    #         if Math.sqrt(number)

    else:
        return "Query does not exist"
