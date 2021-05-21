from spreadsheet.utility import get_user_ccas, is_registered, register_user
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

CCA = 1
SECOND = 2


def start(update, context):
    username = update.message.from_user.username
    first_name = update.message.from_user.first_name
    logger.info("User %s started the conversation.", first_name)

    if is_registered(username):
        ccas = get_user_ccas(username)

        keyboard = [[InlineKeyboardButton(
            cca, callback_data=cca)] for cca in ccas]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text("Hi %s! Please select one of your CCAs." % (
            first_name), reply_markup=reply_markup)
        return CCA
    else:
        update.message.reply_text(
            'Sorry, you are not a registered user. Please contact your CCA Head to register you or /register here.')


def back(update, context):
    query = update.callback_query
    username = query.from_user.username
    first_name = query.from_user.first_name

    ccas = get_user_ccas(username)

    keyboard = [[InlineKeyboardButton(
        cca, callback_data=cca)] for cca in ccas]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text("Hi %s! Please select one of your CCAs." % (
        first_name), reply_markup=reply_markup)
    return CCA


def end(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Ok, see you next time!")
    return ConversationHandler.END
