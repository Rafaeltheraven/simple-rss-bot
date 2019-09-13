# simple-rss-bot
A simple telegram bot to notify you on your rss feeds

# Setup
There are 2 files you need to populate. `urls` and `token`.

## urls
`urls` holds the urls to all your rss feeds, 1 feed per line, nothing more should be added.

## token
The first line of `token` should hold your bot token, the second line should hold your chat id.

# Schedule
Simply run `bot.py` through a cronjob or some other scheduling system.

# Install
Simply run `pip install -r requirements.txt`

On initial run, no messages will be send through Telegram, this is to prevent you from being spammed
by hundreds of "new" messages when you have just added a new feed. If you see the `simple.db` file
in your folder, then everything should be working properly.

This program has only been tested on Python 3
