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

This program has only been tested on Python 3
