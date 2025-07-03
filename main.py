import telebot
from flask import Flask
from threading import Thread
import time
import random
import schedule
import datetime
import os

TOKEN = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(TOKEN)
user_curhat = {}

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

TARGET_CHAT_IDS = [5379888876, 989898123]

def notifikasi_bot_hidup():
    waktu_jakarta = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
    pesan = f"🔄 Bot aktif kembali ({waktu_jakarta.strftime('%Y-%m-%d %H:%M')} WIB). Maaf kalau sempat mati 🙏"
    for user_id in TARGET_CHAT_IDS:
        bot.send_message(user_id, pesan)

notifikasi_bot_hidup()

def kirim_pesan_pagi():
    pesan_list = ["Selamat pagi! Semangat ya 😊", "Pagi, jangan lupa sarapan!"]
    for uid in TARGET_CHAT_IDS:
        bot.send_message(uid, random.choice(pesan_list))

def kirim_pesan_siang():
    pesan_list = ["Selamat siang! Istirahat sejenak 🍛", "Siang ya, jangan lupa makan!"]
    for uid in TARGET_CHAT_IDS:
        bot.send_message(uid, random.choice(pesan_list))

def kirim_pesan_malam():
    pesan_list = ["Selamat malam 🌙 Istirahat ya", "Malam, jangan lupa doa dulu 😊"]
    for uid in TARGET_CHAT_IDS:
        bot.send_message(uid, random.choice(pesan_list))

# Jadwal (UTC untuk WIB)
schedule.every().day.at("23:00").do(kirim_pesan_pagi)
schedule.every().day.at("05:00").do(kirim_pesan_siang)
schedule.every().day.at("15:00").do(kirim_pesan_malam)

def scheduler_loop():
    while True:
        schedule.run_pending()
        time.sleep(1)

Thread(target=scheduler_loop).start()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Halo! Aku Salsa 😘 ketik /help ya kalau butuh bantuan!")

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, "📌 Perintah:\n/help\n/kangen\n/curhat")

@bot.message_handler(commands=['kangen'])
def kangen(message):
    bot.reply_to(message, "Aku juga kangen kamu 🥺")

@bot.message_handler(commands=['curhat'])
def curhat(message):
    user_curhat[message.from_user.id] = True
    bot.reply_to(message, "Silakan curhat... aku dengerin 😊")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    uid = message.from_user.id
    if user_curhat.get(uid):
        with open(f"curhat_{uid}.txt", "a") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message.text}\n")
        bot.reply_to(message, "Terima kasih sudah curhat 🤍")
        user_curhat[uid] = False

bot.infinity_polling(timeout=10, long_polling_timeout=5)
