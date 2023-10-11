import datetime
import logging
import threading

import requests
import schedule
from telegram import ForceReply, Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler
from timetable import DB
from work_api import API

# Enable logging
# logging.basicConfig(filename='logging.log',
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
#                     )
k1 = InlineKeyboardButton('Помощь', callback_data='ок')
k2 = InlineKeyboardButton('Стоп', callback_data='ок')
control_DB = DB()
# logger = logging.getLogger(__name__)
reply_keyboard = [[k1, k2]]
markup = InlineKeyboardMarkup(reply_keyboard)
TOKEN = "5342995443:AAEBqyRLrd5AmHEEhCNLyfHVy3td3Qvw-Ec"
SUPER_PASSWORD_ST = '888'
SUPER_PASSWORD_AD = '111'


def threat():  # второй поток для рассылки
    while True:
        schedule.run_pending()

def pprint(inputi, name, text):
    # logger.info(str(inputi) + str(text) + str(name))
    print(str(inputi), str(text), str(name))

def SendMessage(id, text, token):
    zap = f'''https://api.telegram.org/bot{token}/sendMessage'''
    params = {'chat_id': id, 'text': text}
    return requests.get(zap, params=params).json()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):  # старт
    print(00, control_DB.is_check(update.message.id))
    if control_DB.is_check(update.message.id):
        text = 'Вы уже зарегистрированы.'
        await update.message.reply_text(text)
        pprint('/start', update.message.chat.username, text)
        return ConversationHandler.END
    text = f'Привет! Я смогу тебя отметить, но сначала зарегайся!\nВеди имя и фамилию плиз.'
    pprint('/start', update.message.chat.username, text)
    await update.message.reply_text(text)
    return 1

async def stop_reg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = 'Регистрация отменена.'
    await update.message.reply_text(text, reply_markup=markup)
    pprint('/stop', update.message.chat.username, text)
    return ConversationHandler.END

async def password_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == 'Стоп':
        await update.message.reply_text('Процесс остановлен.')
        return ConversationHandler.END
    fi = update.message.text
    if fi == SUPER_PASSWORD_ST:
        context.user_data['pass'] = 1
        text = "Ок, теперь рили имя"
        await update.message.reply_text(text)
        return 2
    if fi == SUPER_PASSWORD_AD:
        text = 'Ок, теперь рил имя'
        context.user_data['pass'] = 2
        await update.message.reply_text(text)
        return 2
    context.user_data['name'] = fi
    control_DB.add_user(context.user_data['name'], 0, update.message.chat.id)
    text = f'Успешно! {context.user_data["name"]} вы зарегистрированы.'
    await update.message.reply_text(text)
    return ConversationHandler.END
async def final_reg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    control_DB.add_user(update.message.text, context.user_data['pass'], update.message.chat.id)
    text = f'Успешно! {context.user_data["name"]} вы зарегистрированы.'
    await update.message.reply_text(text)
    return ConversationHandler.END

def restart_schedule():
    api.regenerate()
    day = api.get_today()
    time1 = '20:20'
    for i in day:
        time1 = min(i[0], time1)
    print()

if __name__ == '__main__':
    para = []
    api = API()
    application = Application.builder().token(TOKEN).build()
    schedule.every().day.at("06:50").do(restart_schedule)  # рассылка уведомлений
    threading.Thread(target=threat).start()
    # сценарии
    script_registration = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('start', start)],
        # Состояние внутри диалога.
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, password_request)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, final_reg)]

        },
        # Точка прерывания диалога. В данном случае — команда /stop.
        allow_reentry=False,
        fallbacks=[CommandHandler('stop', stop_reg)]
    )
    application.add_handler(script_registration)
    application.run_polling()