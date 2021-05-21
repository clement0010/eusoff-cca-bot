import os
from dotenv import load_dotenv

import logging
from telegram.ext import Updater, ConversationHandler, CommandHandler, CallbackQueryHandler, MessageHandler, CallbackContext, Filters
from telegram_repository.cca import cca
from telegram_repository.utility import start, end, back
from telegram_repository.register import register, startRegister, select_cca, select_category, end_register, clear
from telegram_repository.member import get_member, reply_meeting, member_attendance
from telegram_repository.head import add_member, request_meeting, check_attendance, schedule_meeting, get_attendance

load_dotenv()

PORT = int(os.environ.get('PORT', '8443'))

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = os.getenv('TOKEN')
MODE = os.getenv('MODE')

FIRST, CCA, SECOND = range(3)
REGISTER, SELECT, END = range(3)


def error(update, context):
    logger.warning("Update '%s' caused error '%s'", update, context.error)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [
                CallbackQueryHandler(cca, pattern='^START$'),
                CallbackQueryHandler(end, pattern='^END$')
            ],
            CCA: [
                CallbackQueryHandler(cca)
            ],
            SECOND: [
                # MessageHandler(request_meeting),
                # CallbackQueryHandler(check_attendance),
                CallbackQueryHandler(
                    request_meeting, pattern='^REQUEST_MEETING$'),
                CallbackQueryHandler(
                    check_attendance, pattern='^CHECK_ATTENDANCE$'),
                CallbackQueryHandler(
                    member_attendance, pattern='^GET_ATTENDANCE$'),
                CallbackQueryHandler(
                    get_attendance, pattern='^MEMBER_ATTENDANCE'),
                CallbackQueryHandler(get_member, pattern='^ADD_MEMBER$'),
                CallbackQueryHandler(back, pattern='^BACK$'),
                # Split this out for better UI
                MessageHandler(Filters.regex(
                    '(Head|Team Manager|Member)$'), add_member),
                MessageHandler(Filters.regex(
                    '[0-3]{1}[0-9]{1}/[0-1]{1}[0-9]{1}/2021'), schedule_meeting),
                # CallbackQueryHandler(mark_attendance)
            ],
        },
        allow_reentry=True,
        fallbacks=[CommandHandler('start', start)],
    )

    register_handler = ConversationHandler(
        entry_points=[CommandHandler('register', startRegister)],
        states={
            REGISTER: [
                MessageHandler(Filters.regex(
                    '[A-E]{1}[1-4]{1}[0-9]{2}'), register),
            ],
            SELECT: [
                CallbackQueryHandler(select_cca, pattern="^SELECT-"),
                CallbackQueryHandler(
                    select_category, pattern='(SPORTS|CULTURE|SOCIAL|COMMITTEES|DANCE PRODUCTION)'),
                CallbackQueryHandler(back, pattern='^BACK$'),
                CallbackQueryHandler(clear, pattern="^CLEAR$"),
                CallbackQueryHandler(end_register, pattern='^END$'),
            ],
            END: [
                CallbackQueryHandler(end_register, pattern='^CONFIRM$'),
                CallbackQueryHandler(back, pattern='^BACK$'),
            ]
        },
        fallbacks=[CommandHandler('register', register)],
        allow_reentry=True
    )
    unknown_handler = MessageHandler(Filters.command, unknown)

    dispatcher.add_handler(conversation_handler)
    dispatcher.add_handler(register_handler)
    dispatcher.add_handler(CallbackQueryHandler(
        reply_meeting, pattern='^MEETING-'))
        
    dispatcher.add_handler(unknown_handler)

    dispatcher.add_error_handler(error)

    if MODE == 'DEV':
        updater.start_polling()
    if MODE == 'PROD':
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
        updater.bot.setWebhook('https://eusoff-cca-bot-v2.herokuapp.com/' + TOKEN)

    updater.idle()


if __name__ == '__main__':
    main()
