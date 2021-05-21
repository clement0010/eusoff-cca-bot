# eusoff-cca-bot
All all-in-one solution for Eusoffians to manage their hall commitments.\
\
[Link to Telegram bot](t.me/EusoffCCA_Bot).\
\
## Built With
1. [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library 
2. [Google Sheets API](https://docs.gspread.org/en/latest/index.html)
3. Hosted on [Heroku](https://dashboard.heroku.com/apps).

## Requirements
1. Python 3.8+
## Installation and Setup
1. Set up python virtual environment with `virtualenv <environment_name>`
2. Activate python virtual environment with `source ./<environment_name>/Scripts/activate`
3. Install the required python packages with `pip3 install -r requirements.txt`
4. Run the script `bot.py` with `python3 bot.py`
5. Create a .env file and copy the value from secret.txt

## Configuration
1. Add `.env ` file
2. Include TOKEN = `TELEBOT TOKEN`, MODE = `DEVELOPEMENT OR PRODUCTION`

## Spreadsheet Configuration
1. Setup google service account. [Link to Documentation](https://docs.gspread.org/en/latest/oauth2.html#for-bots-using-service-account)
2. Reminder to include credentials.json in .gitignore (Never expose credential key to public unless github repo is private)
## Testing
1. To test spreadsheet function run `python ./path/to/spreadsheet/function.py`

## Commands
`/start` - Starts the bot
