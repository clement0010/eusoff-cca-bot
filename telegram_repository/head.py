# from spreadsheet.head import
from spreadsheet.head import get_all_cca_members_id, add_date, get_attendance_date_list, get_attedance
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot, Chat
from telegram.ext import ConversationHandler
import logging
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

FIRST = 0
SECOND = 2


def add_member(update, context):
    cca = context.user_data['cca'] 
    member = update.message.text.split(', ')
    # write(cca, member)
    keyboard = [
        [
            InlineKeyboardButton('Go Back', callback_data='START'),
            InlineKeyboardButton("I'm Done", callback_data='END')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "Member successfully added! Is there anything else you want to do?", reply_markup=reply_markup)
    return FIRST


def check_attendance(update, context):
    # Insert the logic here
    cca = context.user_data['cca']
    query = update.callback_query
    query.answer()

    dates = get_attendance_date_list(cca)

    if len(dates) == 0:
        keyboard = [
            [
                InlineKeyboardButton('Request Meeting', callback_data='REQUEST_MEETING'),
            ]
         ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        query.edit_message_text("*[%s ATTENDANCE]* \n\n No meeting scheduled yet!" % (
            cca), reply_markup=reply_markup)

        return SECOND

    keyboard = [[InlineKeyboardButton(
    date, callback_data="MEMBER_ATTENDANCE_"+date)] for date in dates]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text("*Select a date*",
                                reply_markup=reply_markup, parse_mode='Markdown')

    return SECOND

def get_attendance(update, context):
    cca = context.user_data['cca']
    query = update.callback_query
    date = query.data.split('_')[2]
    query.answer()

    logger.info("Getting attendance... CCA: %s Date: %s" % (cca, date))
    data = get_attedance(cca, date)

    member_attendance = data[0]
    total_attendance = data[1]

    text = "*[%s %s ATTENDANCE]*\n" % (cca, date)

    if len(member_attendance) == 0:
        query.edit_message_text(text + "No attendance recorded yet.", parse_mode='Markdown')
        return

    for attendance in data[0]:
        text = text + "%s %s \n" % (attendance[0], attendance[1])

    text = text + '\n' + "Total: " + str(data[1][0])
    query.edit_message_text(text, parse_mode='Markdown')


def request_meeting(update, context):
    cca = context.user_data['cca']
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="*[SCHEDULE MEETING]* Please schedule a meeting date time.\nEg. 02/03/2021",  parse_mode='Markdown')

    return SECOND


def schedule_meeting(update, context):
    date = update.message.text
    cca = context.user_data['cca']
    bot = Bot(token=TOKEN)
    keyboard = [
        [
            InlineKeyboardButton(
                'Can make it =D', callback_data='MEETING-CAN-'+cca+'-'+date),
            InlineKeyboardButton(
                "Can't make it", callback_data='MEETING-CANNOT-'+cca+'-'+date)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    add_date(cca, date)
    chat_id_list = get_all_cca_members_id(cca)

    for chat_id in chat_id_list:
        bot.send_message(chat_id=chat_id, text="*[%s Meeting]*\nAre you attending the meeting on %s" % (
            cca, date), reply_markup=reply_markup, parse_mode='Markdown')
