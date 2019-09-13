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
	c.execute('''CREATE TABLE feeds (ID INTEGER PRIMARY KEY, URL VARCHAR(2083) UNIQUE);''')
	c.execute('''CREATE TABLE entries (ID INTEGER PRIMARY KEY, Feed INTEGER, Title VARCHAR(2083) UNIQUE, FOREIGN KEY(Feed) REFERENCES feeds(ID));''')
	conn.commit()
	conn.close()

def check_new(conn, url, title):
	c = conn.cursor()
	sql = "SELECT ID FROM feeds WHERE URL = ?"
	c.execute(sql, [url])
	ids = c.fetchone()
	new = True
	if not ids:
		sql = "INSERT INTO feeds (URL) VALUES (?);"
		c.execute(sql, [url])
		sql = "INSERT INTO entries (Feed, Title) VALUES (?, ?);"
		c.execute(sql, [c.lastrowid, title])
	else:
		sql = "SELECT Title FROM entries WHERE Feed = ?"
		c.execute(sql, [ids[0]])
		result = c.fetchall()
		for res in result:
			if res[0] == title:
				new = False
				break
		if new:
			sql = "INSERT INTO entries (Feed, Title) VALUES (?, ?);"
			c.execute(sql, [ids[0], title])
	conn.commit()
	return new

def check_feed():
	conn = connect_to_db()
	with open("urls") as f:
		content = f.readlines()
		content = [x.strip() for x in content]

	bot, chat = init_bot()

	for url in content:
		if url == "":
			continue
		feed = feedparser.parse(url)
		for entry in feed['entries']:
			title = entry.title
			desc = entry.description
			link = entry.link
			if check_new(conn, url, title):
				message = "**" + feed.feed.title + "** \n \n"
				message += "[" + title + "](" + link + ") \n \n"
				parsed = feedparser.parse(desc)
				try:
					src = parsed['feed']['img']['src']
					if len(message) > 1024:
						message = message[:1020]
						message += "..."
					bot.send_photo(chat_id=chat, photo=src, caption=message, parse_mode=telegram.ParseMode.MARKDOWN)
				except:	
					tmp = message + html2markdown.convert(feed.entries[0].description)
					try:
						send_message(tmp, bot, chat)
					except:
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