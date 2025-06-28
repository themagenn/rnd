from flask import Flask, request
import telebot
import random

API_TOKEN = "7860631728:AAEvQBS0DXvp-F0Xor7PLorjEp5uMZETk0w"
OWNER_ID = 6697710886
WEBHOOK_URL = "https://dmag22.pythonanywhere.com/"  # Твой поддомен

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

one_time_number = None

# Команда /random
@bot.message_handler(commands=['random'])
def handle_random(message):
    global one_time_number
    number = one_time_number if one_time_number is not None else random.randint(1, 100)
    one_time_number = None
    sender = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
    bot.send_message(message.chat.id, f"Պատահական Թիվ: {number}\nՀրամանը ուղարկեց՝ {sender}")

# Скрытое число (только для тебя)
@bot.message_handler(func=lambda msg: msg.from_user.id == OWNER_ID and msg.text.isdigit())
def set_secret_number(message):
    global one_time_number
    number = int(message.text)
    if 1 <= number <= 100:
        one_time_number = number
        bot.send_message(message.chat.id, "Թիվը պահպանված է։ Կցուցադրվի հաջորդ /random հրամանից")

# Обработка входящих webhook-запросов
@app.route('/', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# Установка webhook (один раз)
@app.route('/setwebhook', methods=['GET'])
def set_webhook():
    success = bot.set_webhook(url=WEBHOOK_URL)
    return "OK" if success else "Webhook setup failed", 200

if __name__ == "__main__":
    app.run()
