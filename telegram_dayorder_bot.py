from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from datetime import datetime, timedelta
import threading
import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
# === CONFIG ===


# === TIMETABLE ===
TIMETABLE = {
    "Day 1": [("8:00 AM", "CN"), ("8:50 AM", "CN"), ("9:45 AM", "ML"), ("10:40 AM", "ML"),
              ("11:35 AM", "SWC"), ("12:30 PM", "eat food"), ("1:25 PM", "do class work"),
              ("2:20 PM", "do class work"), ("3:10 PM", "do ai python course"),
              ("4:00 PM", "do ai python course"), ("5:00 PM", "snacks + exercise"),
              ("6:00 PM", "NPTEL ML"), ("7:00 PM", "NPTEL ML"), ("8:00 PM", "eat food bro"),
              ("9:00 PM", "DSA")],
    "Day 2": [("8:00 AM", "Fresh up"), ("8:50 AM", "Food + do incomplete work"),
              ("9:45 AM", "do ai python course"), ("10:40 AM", "do ai python course"),
              ("11:35 AM", "eat food"), ("12:30 PM", "FSWD"), ("1:25 PM", "FSWD"),
              ("2:20 PM", "SWC"), ("3:10 PM", "SWC"), ("4:00 PM", "Break"),
              ("5:00 PM", "snacks + exercise"), ("6:00 PM", "NPTEL ML"), ("7:00 PM", "NPTEL ML"),
              ("8:00 PM", "eat food bro"), ("9:00 PM", "DSA")],
    "Day 3": [("8:00 AM", "DM"), ("8:50 AM", "DM"), ("9:45 AM", "CN"), ("10:40 AM", "FLAA"),
              ("11:35 AM", "FSWD"), ("12:30 PM", "eat food"), ("1:25 PM", "do ai python course"),
              ("2:20 PM", "do ai python course"), ("3:10 PM", "academic work"),
              ("4:00 PM", "academic work"), ("5:00 PM", "snacks + exercise"),
              ("6:00 PM", "NPTEL ML"), ("7:00 PM", "NPTEL ML"), ("8:00 PM", "eat food bro"),
              ("9:00 PM", "DSA"), ("11:59 PM", "Testing")],
    "Day 4": [("8:00 AM", "Fresh up"), ("8:50 AM", "incomplete work"), ("9:45 AM", "Ai python course"),
              ("10:40 AM", "Ai python course"), ("11:35 AM", "eat food"), ("12:30 PM", "FLAA"),
              ("1:25 PM", "FLAA"), ("2:20 PM", "FSWD"), ("3:10 PM", "break"), ("4:00 PM", "DM"),
              ("5:00 PM", "snacks + exercise"), ("6:00 PM", "NPTEL ML"), ("7:00 PM", "NPTEL ML"),
              ("8:00 PM", "eat food bro"), ("9:00 PM", "DSA")],
    "Day 5": [("8:00 AM", "Fresh up"), ("8:50 AM", "incomplete work"), ("9:45 AM", "DM"),
              ("10:40 AM", "ML"), ("11:35 AM", "FLAA"), ("12:30 PM", "eat food"),
              ("1:25 PM", "DO CN LAB WORK"), ("2:20 PM", "DO CN LAB WORK"),
              ("3:10 PM", "CN LAB"), ("4:00 PM", "CN LAB"), ("5:00 PM", "snacks + exercise"),
              ("6:00 PM", "Ai python course"), ("7:00 PM", "NPTEL ML"), ("8:00 PM", "eat food bro"),
              ("9:00 PM", "DSA")],
    "Saturday": [("8:00 AM", "Fresh up"), ("8:50 AM", "incomplete work"),
                 ("9:45 AM", "Ai python course"), ("10:40 AM", "Ai python course"),
                 ("11:35 AM", "EAT FOOD"), ("12:30 PM", "Project work"),
                 ("1:25 PM", "Project work"), ("2:20 PM", "Project work"),
                 ("3:10 PM", "NPTEL ML"), ("4:00 PM", "NPTEL ML"),
                 ("5:00 PM", "snacks + exercise"), ("6:00 PM", "O.S"),
                 ("7:00 PM", "O.S"), ("8:00 PM", "eat food bro"), ("9:00 PM", "DSA")],
    "Sunday": [("8:00 AM", "Fresh up"), ("8:50 AM", "incomplete work"),
               ("9:45 AM", "Ai python course"), ("10:40 AM", "Ai python course"),
               ("11:35 AM", "EAT FOOD"), ("12:30 PM", "Project work"),
               ("1:25 PM", "Project work"), ("2:20 PM", "Project work"),
               ("3:10 PM", "NPTEL ML"), ("4:00 PM", "NPTEL ML"),
               ("5:00 PM", "snacks + exercise"), ("6:00 PM", "O.S"),
               ("7:00 PM", "O.S"), ("8:00 PM", "eat food bro"), ("9:00 PM", "DSA")],
}

# === START MESSAGE ===
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Day 1", callback_data='Day 1'),
         InlineKeyboardButton("Day 2", callback_data='Day 2'),
         InlineKeyboardButton("Day 3", callback_data='Day 3')],
        [InlineKeyboardButton("Day 4", callback_data='Day 4'),
         InlineKeyboardButton("Day 5", callback_data='Day 5')],
        [InlineKeyboardButton("Saturday", callback_data='Saturday'),
         InlineKeyboardButton("Sunday", callback_data='Sunday')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("🌞 Good morning! Please select today's Day Order:", reply_markup=reply_markup)

# === SCHEDULE REMINDERS ===
def schedule_reminders(day):
    now = datetime.now()
    for time_str, subject in TIMETABLE[day]:
        class_time = datetime.strptime(time_str, "%I:%M %p").replace(
            year=now.year, month=now.month, day=now.day)
        alert_time = class_time - timedelta(minutes=5)
        delay = (alert_time - now).total_seconds()
        if delay > 0:
            threading.Timer(delay, Bot(BOT_TOKEN).send_message,
                            args=(CHAT_ID, f"🔔 Reminder: {subject} starts at {time_str}",)).start()

# === HANDLE SELECTION ===
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    selected_day = query.data
    query.answer()
    query.edit_message_text(f"✅ You selected {selected_day}. Notifications will be sent.")
    schedule_reminders(selected_day)

# === MAIN ===
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
