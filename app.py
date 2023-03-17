import os

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
from telegram_bot import start
import openai


load_dotenv()


OPEN_API_KEY = os.getenv("OPENAI_API_KEY")
OPEN_ORG_ID = os.getenv("OPENAI_ORG_ID")

openai.organization = OPEN_ORG_ID
openai.api_key = OPEN_API_KEY


app = Flask(__name__)


@app.route("/", methods=("GET", "POST"))
def index():
    question = ""
    if request.method == "POST":
        question = request.form["question"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=question,
            temperature=0.6,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result, question=question)
