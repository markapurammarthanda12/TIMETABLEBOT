import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
import datetime
import threading

# ============================== YOUR DETAILS ==============================
BOT_TOKEN = "8287025689:AAGmQV3ffIv_jcaJl_H6L_nHfv55wFasPJg"
CHAT_ID = 5718210858
# ==========================================================================

# Your full schedule for each Day Order
DAY_SCHEDULES = {
    "Day 1": [("8:00 AM", "Computer Networks"), ("10:40 AM", "Machine Learning"), ("12:40 PM", "Python"), ("7:00 PM", "Academic Work")],
    "Day 2": [("8:00 AM", "Maths"), ("10:40 AM", "Python"), ("12:40 PM", "Mini Project"), ("7:00 PM", "Academic Work")],
    "Day 3": [("8:00 AM", "OS"), ("10:40 AM", "Python"), ("12:40 PM", "DSA"), ("7:00 PM", "Academic Work")],
    "Day 4": [("10:40 AM", "ML"), ("12:40 PM", "CN Lab"), ("3:00 PM", "Open Slot"), ("7:00 PM", "Academic Work")],
    "Day 5": [("9:00 AM", "Python Lab"), ("11:40 AM", "ML"), ("2:40 PM", "Mini Project"), ("7:00 PM", "Academic Work")],
    "Saturday": [("10:00 AM", "Project Work"), ("3:00 PM", "Hackathon Prep"), ("7:00 PM", "Academic Work")],
    "Sunday": [("9:00 AM", "Practice DSA"), ("2:00 PM", "Mini Project Work"), ("7:00 PM", "Review + Rest")]
}

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Send inline button menu to user
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton(day, callback_data=day)] for day in DAY_SCHEDULES.keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('🌞 Good morning! Please select today’s Day Order:', reply_markup=reply_markup)

# When user taps on Day Order button
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    selected_day = query.data
    query.edit_message_text(text=f"✅ Got it! You selected: *{selected_day}*\nYou'll get reminders!", parse_mode='Markdown')

    # Schedule class reminders
    for time_str, subject in DAY_SCHEDULES[selected_day]:
        schedule_reminder(time_str, subject, context)

# Schedule a reminder for a specific time
def schedule_reminder(time_str, subject, context: CallbackContext):
    try:
        class_time = datetime.datetime.strptime(time_str, "%I:%M %p").time()
        now = datetime.datetime.now()
        reminder_time = datetime.datetime.combine(now.date(), class_time) - datetime.timedelta(minutes=5)
        if reminder_time < now:
            return  # Skip if time already passed

        delay = (reminder_time - now).total_seconds()
        threading.Timer(delay, send_reminder, args=(subject, time_str, context)).start()
    except Exception as e:
        logger.error(f"Failed to schedule reminder for {subject}: {e}")

# Send the reminder message
def send_reminder(subject, time_str, context: CallbackContext):
    try:
        context.bot.send_message(chat_id=CHAT_ID, text=f"🔔 Reminder: *{subject}* starts at {time_str}", parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Failed to send reminder: {e}")

# Main function
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
