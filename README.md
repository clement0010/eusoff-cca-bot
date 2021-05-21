# eusoff-cca-bot
All all-in-one solution for Eusoffians to manage their hall commitments.\
\
[Link to Telegram bot](t.me/EusoffCCA_Bot).\
\
Built using the [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library and [Google Sheets API](https://developers.google.com/sheets/api/quickstart/python).\
Hosted on [Heroku](https://dashboard.heroku.com/apps).

## Requirements
1. Python 3.8+
## Installation and Setup
1. Set up python virtual environment with `virtualenv <environment_name>`
2. Activate python virtual environment with `source ./<environment_name>/Scripts/activate`
3. Install the required python packages with `pip3 install -r requirements.txt`
4. Run the script `bot.py` with `python3 bot.py`
5. Create a .env file and copy the value from secret.txt

## Testing
1. To test spreadsheet function run `python ./path/to/spreadsheet/function.py`

## Commands
`/start` - Starts the bot

## Flow
1. Upon start, the bot will check if you are a registered user, and then list out all your CCAs
2. Upon selecting a CCA, bot will check your position (i.e. Head, Team Manager, Member) and present you a list of available actions
3. Select the action you want to do, then start again or end the conversation

## Actions

### Head 
Committee Heads and Vice-Heads, Sports Captains and Vice-Captains.
#### Request Meeting (WIP)
1. User inputs a meeting date and time (e.g. 14/02/21 1400-1500).
2. A notification gets sent to all members asking for their availability (i.e yes / no).
3. User gets a count of how many members will be able to make it for the meeting.
#### Check Attendance (WIP)
1. User receives his/her attendance count.
#### Add Member
1. User inputs the full name, telegram username and position of the incoming member (i.e John Tan, john123, Member). Note that the entries have to be comma separated, and the position entry can only be 'Head', 'Team Manager' or 'Member'.
2. New member's details are appended to the spreadsheet and the user receives a reply saying that the new member has been added successfully. 
3. User can do another action or end the conversation.

### Team Manager
Non-sports CCAs can appoint someone to mark attendance.
#### Mark Attendance (WIP)
1. User inputs the training date and time (i.e. 14/02/21 1400-1600).
2. User receives a list of all members' names.
3. User presses the names of all members present at training to mark them as present on the spreadsheet.
4. User presses the 'Done' button at the bottom of the list to finish marking attendance.
5. User can start again or end the conversation.
### Member
For the normies.
#### Check Attendance (WIP)
1. User receives his/her attendance count.
