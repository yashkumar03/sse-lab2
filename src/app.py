from flask import Flask, render_template, request
import re
import math
import requests
import os

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
    q = request.args.get("q", "")
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


# employed token to increase the api request rate limit
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": f"token{GITHUB_TOKEN}"}


@app.route("/github", methods=["GET", "POST"])
def github_info():
    if request.method == "POST":
        username = request.form.get("username", "")
        link = f"https://api.github.com/users/{username}/repos"
        response = requests.get(link, headers=headers)

        # if out of tokens give user a response
        if response.status_code != 200:
            return f"{response.status_code}: {response.reason}"
        # if valid response, fetch more data from API
        if response.status_code == 200:
            # data returned is a list of 'repository' entities
            repos = response.json()
            for i, repo in enumerate(repos):
                commits_url = repo["commits_url"].replace("{/sha}", "")
                response_commit = requests.get(commits_url)
                if response_commit.status_code == 200:
                    commit = response_commit.json()

                    if commit:
                        repos[i]["latest_commit"] = {
                            "sha": commit[0]["sha"],
                            "author": commit[0]["commit"]["author"]["name"],
                            "date": commit[0]["commit"]["author"]["date"],
                            "message": commit[0]["commit"]["message"],
                            "url": f"""
                            https://github.com/{username}/{repo['name']}
                            """,
                        }
            return render_template("github_table.html", repos=repos)

    return render_template("github_route.html")
