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


def process_query(query: str):
    if query == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"

    elif query == "asteroids":
        return "Unknown"

    elif "What is" in query and "multiplied" in query:
        numbers = re.findall(r"\d+", query)
        numbers = [int(num) for num in numbers]
        return str(numbers[0] * numbers[1])

    elif "What is" in query and "plus" in query:
        numbers = re.findall(r"\d+", query)
        numbers = [int(num) for num in numbers]
        return str(numbers[0] + numbers[1])

    elif "What is" in query and "minus" in query:
        numbers = re.findall(r"\d+", query)
        numbers = [int(num) for num in numbers]
        return str(numbers[0] - numbers[1])

    elif "Which of the following numbers is the largest" in query:
        numbers = re.findall(r"\d+", query)
        numbers = [int(num) for num in numbers]
        return str(max(numbers))

    elif "Which of the following numbers are primes" in query:
        numbers = re.findall(r"\d+", query)
        numbers = [int(num) for num in numbers]
        prime_list = ""
        for number in numbers:
            isPrime = True
            for i in range(2, round(math.sqrt(number)) + 1):
                if number % i == 0:
                    isPrime = False
                    break
            if isPrime:
                prime_list = prime_list + str(number) + ", "
        return prime_list[:-2]

    elif "Which of the following numbers is both a square and a cube" in query:
        numbers = re.findall(r"\d+", query)
        numbers = [int(num) for num in numbers]
        for number in numbers:
            sixth_root = round(number ** (1 / 6))
            if sixth_root**6 == number:
                return str(number)

    else:
        return "Query does not exist"
