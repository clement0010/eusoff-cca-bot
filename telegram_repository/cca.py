from spreadsheet.utility import get_user_position
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

SECOND = 2


def cca(update, context):
    query = update.callback_query
    username = query.from_user.username
    cca = query.data
    context.user_data['cca'] = cca
    position = get_user_position(username, cca)
    logger.info(position)

    query.answer()
    if position == 'Head':
        keyboard = [
            [InlineKeyboardButton(
                'Request Meeting', callback_data='REQUEST_MEETING')],
            [InlineKeyboardButton('Check Attendance',
                                  callback_data='CHECK_ATTENDANCE')],
            # [InlineKeyboardButton(
            #     'Add Member', callback_data='ADD_MEMBER')],
            [InlineKeyboardButton('Back', callback_data='BACK')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text="Head of %s! What would you like to do?" % (
            cca), reply_markup=reply_markup)
        return SECOND
    elif position == 'Team Manager':
        keyboard = [
            [
                InlineKeyboardButton(
                    'Mark Attendance', callback_data='GET MEMBER')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text="%s's Team manager! What would you like to do?" % (
            cca), reply_markup=reply_markup)
        return SECOND
    else:
        keyboard = [
            [
                InlineKeyboardButton(
                    "Check Attendance", callback_data='GET_ATTENDANCE')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text="You're a member of %s! What would you like to do?" % (
            cca), reply_markup=reply_markup)
        return SECOND
