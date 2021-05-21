from spreadsheet.member import mark_attendance, get_attendance
import logging
from spreadsheet.head import get_all_cca_members_id, add_date

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

CCA = 1
SECOND = 2


def get_member(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        "Please enter the incoming member's full name, telegram username and position, separating each value with commas.\n\n"
        "Note that the position can only be Head, Team Manager or Member.\n\n"
        "e.g. MALERIADO SHEM LIMOS, sheimoria, Member")
    return SECOND


def reply_meeting(update,  context):
    query = update.callback_query
    username = query.message.chat.username

    data = query.data.split('-')
    logger.info(data)
    mark_attendance(username, data)
    query.edit_message_text(
        text="Successfully Replied!\nStart again /start", parse_mode='Markdown')


def member_attendance(update, context):
    query = update.callback_query
    name = query.message.chat.username
    data = get_attendance(name, context.user_data['cca'])
    cca = context.user_data['cca']
    text = "*[" + cca + " ATTENDANCE]*\n"

    query.answer()

    if len(data[0]) == 0:
        query.edit_message_text(text + "No attendance recorded yet.", parse_mode='Markdown')
        return

    for dates in data[0]:
        text = text + dates[0] + " " + str(dates[1]) + '\n'
    text = text + '\n' + "Total: " + str(data[1][0])
    query.edit_message_text(text, parse_mode='Markdown')
