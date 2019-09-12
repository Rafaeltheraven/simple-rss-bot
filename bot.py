import feedparser
import sqlite3
import os
from hashlib import sha1
from json import dumps
import telegram
import html2markdown

def connect_to_db():
	if not os.path.exists('simple.db'):
		create_db()
	return sqlite3.connect('simple.db')

def create_db():
	conn = sqlite3.connect('simple.db')
	c = conn.cursor()
	c.execute('''CREATE TABLE feeds (url VARCHAR(2083) PRIMARY KEY, hash VARCHAR(40));''')
	conn.commit()
	conn.close()

def check_new(conn, feed, has):
	c = conn.cursor()
	sql = "SELECT hash FROM feeds WHERE url = ?;"
	c.execute(sql, [feed])
	ha = c.fetchone()
	new = False
	if not ha:
		sql = "INSERT INTO feeds (url, hash) VALUES (?, ?);"
		c.execute(sql, (feed, has))
		new = True
	elif ha != has:
		sql = "UPDATE feeds SET hash = ? WHERE url = ?;"
		c.execute(sql, (has, feed))
		new = True
	conn.commit()
	return new

def check_feed():
	conn = connect_to_db()
	with open("urls") as f:
		content = f.readlines()
		content = [x.strip() for x in content]

	bot, chat = init_bot()

	for url in content:
		feed = feedparser.parse(url)
		has = sha1(dumps(feed.entries).encode()).hexdigest()
		if check_new(conn, url, has):
			message = "[" + feed.feed.title + "] \n \n"
			message += "[" + feed.entries[0].title + "](" + feed.entries[0].link + ") \n \n"
			desc = feed.entries[0].description
			parsed = feedparser.parse(desc)
			try:
				src = parsed['feed']['img']['src']
				if len(message) > 1024:
					message = message[:1020]
					message += "..."
				bot.send_photo(chat_id=chat, photo=src, caption=message, parse_mode=telegram.ParseMode.MARKDOWN)
			except:	
				message += html2markdown.convert(feed.entries[0].description)
				send_message(message, bot, chat)
	conn.close()

def init_bot():
	with open("token") as f:
		content = f.readlines()
		content = [x.strip() for x in content]
	bot = telegram.Bot(token=content[0])
	return bot, content[1]

def send_message(message, bot, chat):
	if len(message) > 1024:
		message = message[:100]
		message += "..."
	bot.sendMessage(text=message, chat_id=chat, parse_mode=telegram.ParseMode.MARKDOWN)

if __name__ == "__main__":
	init = True
	if not os.path.exists("urls"):
		print("You do not have a urls file, please add your rss feeds to the newly created urls file")
		init = False
	if not os.path.exists("token"):
		print("You do not have a token file, please add the neccessary details to your token file")
		init = False
	if not init:
		exit()
	check_feed()