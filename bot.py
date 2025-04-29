import telebot
import schedule
import time
import datetime
from utils import get_total_players, get_top_3_scores, reset_scores, reset_players, save_player, registered_players

bot_token = '8021015472:AAGcLPvb0k6L-NwkKkWEAabEwZpfRRbO1cA'
group_id = -1002427129658
bot = telebot.TeleBot(bot_token)

game_link = "https://t.me/gamee?game=basketboy"
start_week = 1
current_week = start_week

def get_battle_time_info():
    now = datetime.datetime.now()
    battle_start = now - datetime.timedelta(days=now.weekday())
    battle_start = battle_start.replace(hour=22, minute=0, second=0, microsecond=0)
    if now < battle_start:
        battle_start -= datetime.timedelta(weeks=1)
    elapsed = now - battle_start
    left = datetime.timedelta(weeks=1) - elapsed
    return left, elapsed

def send_late_join_message(chat_id):
    battle_time_left, battle_time_elapsed = get_battle_time_info()

    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    markup.add(
        telebot.types.KeyboardButton("✅ Setuju & Main Sekarang"),
        telebot.types.KeyboardButton("❌ Tunggu Minggu Depan")
    )

    bot.send_message(
        chat_id,
        f"⏳ *Sesi Battle Sudah Bermula!*\n\n"
        f"- Masa berlalu: `{str(battle_time_elapsed).split('.')[0]}`\n"
        f"- Masa tinggal: `{str(battle_time_left).split('.')[0]}`\n\n"
        "Adakah anda mahu teruskan untuk sesi ini?",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: message.text == "✅ Setuju & Main Sekarang")
def handle_accept(message):
    player = message.from_user.username or message.from_user.first_name
    save_player(player)
    bot.send_message(message.chat.id, f"Good luck, {player}! Ini link game kamu:\n{game_link}")
    update_group_status()

@bot.message_handler(func=lambda message: message.text == "❌ Tunggu Minggu Depan")
def handle_decline(message):
    bot.send_message(message.chat.id, "Baik! Jumpa anda minggu depan, Ahad 10.00 PM.")

def update_group_status():
    total_players = len(registered_players)
    prize_pool = total_players * 10
    prize_winner = prize_pool * 0.8
    admin_fee = prize_pool * 0.2
    top_scores = get_top_3_scores()

    text = (
        f"🏆 *RINGGIT FIGHTER (S.{current_week})*\n"
        f"📆 Tarikh: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        f"👤 Jumlah Peserta: {total_players}\n"
        f"💸 Hadiah Pemenang (80%): RM{prize_winner:.2f}\n"
        f"⚡ Kos Admin (20%): RM{admin_fee:.2f}\n\n"
        f"🔥 *Top 3 Skor Semasa:*\n"
        f"1. {top_scores[0]}\n"
        f"2. {top_scores[1]}\n"
        f"3. {top_scores[2]}"
    )
    bot.send_message(group_id, text, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    send_late_join_message(message.chat.id)

def reset_weekly():
    global current_week
    current_week += 1
    reset_scores()
    reset_players()
    registered_players.clear()
    bot.send_message(group_id, f"✨ *Sesi Baru Dimulakan!* (S.{current_week})", parse_mode="Markdown")

def schedule_reset():
    schedule.every().sunday.at("22:00").do(reset_weekly)
    while True:
        schedule.run_pending()
        time.sleep(60)

import threading
threading.Thread(target=schedule_reset).start()

bot.polling()
