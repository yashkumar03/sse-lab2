from flask import Flask, render_template, request
import re
import math
import requests
import json

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
    q = request.args.get('q', '')
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
    
    
@app.route("/github", methods=["GET", "POST"])
def github_info():
    if request.method == "POST":
        username = request.form.get("username", '')
        response = requests.get(f"https://api.github.com/users/{username}/repos")
        if response.status_code == 200:
            repos = response.json() # data returned is a list of ‘repository’ entities
            print(repos[0][])
            # for repo in repos:
            #     reponse_commit = requests.get(f"{repo.commits_url}")
            #     commit_data = response_commit.json()
            #     print(commit_data)
            return render_template("github_table.html", repos=repos)
            
    return render_template("github_route.html")
