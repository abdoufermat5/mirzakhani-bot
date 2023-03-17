import os
from datetime import datetime

import openai
import telebot
from dateutil.tz import gettz
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
import humanize
from service.db_service import getLastFiveRecords, addRecord

load_dotenv()

OPEN_API_KEY = os.getenv("OPENAI_API_KEY")
OPEN_ORG_ID = os.getenv("OPENAI_ORG_ID")
BOT_API_KEY = os.getenv("BOT_API_KEY")

bot = telebot.TeleBot(token=BOT_API_KEY)
bot.set_webhook(url="https://62d7-46-193-64-45.eu.ngrok.io/maryam-bot")
openai.organization = OPEN_ORG_ID
openai.api_key = OPEN_API_KEY

app = Flask(__name__)

conversation = [{"role": "system", "content": "DIRECTIVE_FOR_gpt-3.5-turbo"}]
last5 = getLastFiveRecords()
if len(last5) != 0:
    for record in last5:
        conversation.append({"role": "user", "content": record.question})
        conversation.append({"role": "system", "content": record.answer})


@app.template_filter('time_ago')
def time_ago_filter(time):
    time_difference = datetime.utcnow() - time
    t = humanize.naturaldelta(time_difference)
    return t


@app.route("/maryam-bot", methods=["POST"])
def maryam_bot():
    message = request.json["message"]
    print(message)
    bot.send_message(chat_id=message['chat']["id"], text="Une seconde, je réfléchis...")
    conversation.append({"role": "user", "content": message["text"]})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )
    # envoie la réponse
    addRecord(message["text"], response.choices[0].message.content, response.choices[0].message.role)
    conversation.append({"role": response.choices[0].message.role, "content": response.choices[0].message.content})
    bot.send_message(chat_id=message['chat']["id"], text=response.choices[0].message.content)
    return "ok"


@app.route("/", methods=("GET", "POST"))
def index():
    question = ""
    if request.method == "POST":
        question = request.form["question"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=question,
            temperature=0.6,
            max_tokens=1000,
        )
        # save the question and answer in the database
        addRecord(question, response.choices[0].text, type=2)
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    last5_records = getLastFiveRecords(type=2)
    return render_template("index.html", result=result, question=question, all_answers=last5_records)


if __name__ == "__main__":
    app.run()
