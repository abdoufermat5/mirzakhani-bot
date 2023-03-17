import openai
from dotenv import load_dotenv
import os
import telebot

from service.db_service import addRecord, getLastFiveRecords

load_dotenv()
OPEN_API_KEY = os.getenv("OPENAI_API_KEY")
OPEN_ORG_ID = os.getenv("OPENAI_ORG_ID")

openai.organization = OPEN_ORG_ID
openai.api_key = OPEN_API_KEY
BOT_API_KEY = os.getenv("BOT_API_KEY")

bot = telebot.TeleBot(token=BOT_API_KEY)
conversation = [{"role": "system", "content": "DIRECTIVE_FOR_gpt-3.5-turbo"}]
last5 = getLastFiveRecords()
if len(last5) != 0:
    for record in last5:
        conversation.append({"role": "user", "content": record.question})
        conversation.append({"role": "system", "content": record.answer})


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Salut ! Je suis le bot de Fermat. Je peux t'aider à trouver des réponses à tes "
                          "questions.")


@bot.message_handler(func=lambda message: True)
def answer(message):
    bot.reply_to(message, "Une seconde, je réfléchis...")

    conversation.append({"role": "user", "content": message.text})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )
    # envoie la réponse
    addRecord(message.text, response.choices[0].message.content, response.choices[0].message.role)
    conversation.append({"role": response.choices[0].message.role, "content": response.choices[0].message.content})
    bot.reply_to(message, response.choices[0].message.content)


def start():
    bot.infinity_polling()


if __name__ == "__main__":
    start()
