import telebot
import os

API_TOKEN = os.environ.get("8293559851:AAHF7cy3dRXlgQd896XJDJi9hult6jnq6g8")
bot = telebot.TeleBot(API_TOKEN)

joc_curent = {
    "zi": None,
    "ora": None,
    "jucatori": set()
}

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.lower()

    if "padel" in text and ("vineri" in text or "sambata" in text):
        joc_curent["zi"] = "vineri" if "vineri" in text else "sambata"
        joc_curent["ora"] = "19:00"
        joc_curent["jucatori"] = set()
        bot.reply_to(message, f"Detectat joc de padel {joc_curent['zi']} la {joc_curent['ora']}! Cine vine?")

    elif text in ["eu vin", "vin", "confirm", "sunt in"]:
        username = message.from_user.first_name or message.from_user.username
        joc_curent["jucatori"].add(username)

        if len(joc_curent["jucatori"]) >= 4:
            bot.send_message(
                message.chat.id,
                f"🎾 Avem minim 4 jucători pentru padel {joc_curent['zi']} la {joc_curent['ora']}! "
                f"Participanți: {', '.join(joc_curent['jucatori'])}\n"
                f"👉 Fac acum rezervarea!"
            )
        else:
            bot.send_message(
                message.chat.id,
                f"{username} confirmat. Total: {len(joc_curent['jucatori'])} jucători."
            )

bot.infinity_polling()
