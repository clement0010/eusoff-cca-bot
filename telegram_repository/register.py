from spreadsheet.utility import get_user_ccas, is_registered, register_user, get_ccas_by_category
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CallbackQueryHandler
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

REGISTER = 0
SELECT = 1
END = 2

# def back(update, context):
#     return SECOND


def startRegister(update, context):
    context.user_data['user_data'] = []
    context.user_data['cca_list'] = []

    username = update.message.from_user.username

    if is_registered(username):
        update.message.reply_text(
            'You have registered. Please /start to begin.')
        return ConversationHandler.END
    else:
        update.message.reply_text("Please enter your full name and room number, separating each value with commas.\n\n"
                                  "e.g. John, A101")

        return REGISTER


def register(update, context):
    # if 'previous_page' in context.user_data.keys():
    #     context.user_data['register_page'].append(context.user_data['previous_page'])
    context.user_data['user_data'] = update.message.text.split(',')

    keyboard = [
        [InlineKeyboardButton('DANCE PRODUCTION',
                              callback_data='DANCE PRODUCTION')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("*Select your CCAs* \n\nWhich category is your CCA in?",
                              reply_markup=reply_markup, parse_mode='Markdown')

    return SELECT


def select_category(update, context):

    query = update.callback_query
    cca_string = 'You have not selected a CCA.'
    if 'cca_list' in context.user_data.keys():
        cca_string = 'You have selected ' + \
            ', '.join(context.user_data['cca_list']) + '.'

    category = query.data
    query.answer()

    category = 'SOCIAL SERVICES' if category == 'SOCIAL' else (
        'OTHER COMMITTEES' if category == 'COMMITTEES' else category
    )
    ccas = get_ccas_by_category(category)

    keyboard = [[InlineKeyboardButton(
        cca, callback_data="SELECT-"+cca)] for cca in ccas]
    # keyboard.append([InlineKeyboardButton("Back", callback_data='BACK')])
    text = """*SELECT CCAs* \n\nPlease select your CCA from the *%s* category.\n%s"""
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(text=text % (
        category, cca_string), reply_markup=reply_markup, parse_mode='Markdown')

    return SELECT


def select_cca(update, context):
    query = update.callback_query
    cca_string = ''
    if not 'cca_list' in context.user_data.keys():
        context.user_data['cca_list'] = []
        cca_string = 'You have not selected a CCA.'

    cca = query.data

    cca = cca[7:]

    if len(context.user_data['cca_list']) == 0:

        context.user_data['cca_list'] = [cca]
        cca_string = "You have selected " + cca + "."
    else:
        context.user_data['cca_list'].append(cca)

        cca_string = "You have selected " + \
            ", ".join(context.user_data['cca_list'])

    query.answer()

    keyboard = [
        [InlineKeyboardButton('DANCE PRODUCTION',
                              callback_data='DANCE PRODUCTION')],
        # [InlineKeyboardButton('SPORTS', callback_data='SPORTS')],
        # [InlineKeyboardButton("CULTURE", callback_data='CULTURE')],
        # [InlineKeyboardButton("SOCIAL SERVICES", callback_data='SOCIAL'),
        # [InlineKeyboardButton("OTHER COMMITTEES",
        #                     callback_data = 'COMMITTEES'),
        [InlineKeyboardButton("CLEAR CCA LIST", callback_data='CLEAR')],
        [InlineKeyboardButton("DONE", callback_data='END')]
    ]

    text = """*SELECT CCAs* \n\nPlease select the category of your other CCA.\n%s"""

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(text=text % (cca_string),
                            reply_markup=reply_markup, parse_mode='Markdown')

    return SELECT

# WIP


def clear(update, context):
    query = update.callback_query
    context.user_data['cca_list'] = []
    query.edit_message_text(
        text="Work in progress\n Start again /register", parse_mode='Markdown')

    return SELECT


def back(update, context):
    query = update.callback_query
    context.user_data['cca_list'] = []
    query.edit_message_text(
        text="Work in progress\n Start again /register", parse_mode='Markdown')

    return SELECT


def end_register(update, context):
    query = update.callback_query
    if update.callback_query.data == 'END':
        keyboard = [
            [
                InlineKeyboardButton('CONFIRM', callback_data='CONFIRM'),
                # InlineKeyboardButton("BACK", callback_data='BACK')
            ]
        ]
        user_data = context.user_data['user_data']
        cca_list = ", ".join(context.user_data['cca_list'])
        logger.info(user_data)
        logger.info(cca_list)

        text = """*[CONFIRMATION]*\nPlease confirm and verify your selection.\n*Full Name:* %s\n*Room Number:* %s\n*CCA(s):* %s\n"""

        reply_markup = InlineKeyboardMarkup(keyboard)

        query.edit_message_text(text=text % (
            user_data[0], user_data[1], cca_list), reply_markup=reply_markup, parse_mode='Markdown')

    elif update.callback_query.data == 'CONFIRM':
        user_data = context.user_data['user_data']
        cca_list = context.user_data['cca_list']

        register_user(update.callback_query.message.chat, user_data, cca_list)
        logger.info("Updated sheet")

        query.edit_message_text(
            text="Congratulations %s! You have completed your registration.\nEnter /start to start." % (user_data[0]), parse_mode='Markdown')
        return ConversationHandler.END

    return END
