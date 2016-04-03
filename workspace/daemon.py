import socket, string, oauth
import MySQLdb
import os
import requests
import threading
import re
from csgo import readAPI, checkGame

chatterlist = []
#connect db
db = MySQLdb.connect(os.getenv('IP'), os.getenv('C9_USER'), "", "c9", 3306)
cursor = db.cursor() 

def checkerAPI():
	threading.Timer(15.0, checkerAPI).start()
	with open("results.txt", "r") as myfile:
		for line in myfile:
			if line == "nochange":
				readAPI()
			else:
				break
def readWeb():
	global chatterlist
	url = "http://tmi.twitch.tv/group/user/penquino/chatters"
	threading.Timer(30.0, readWeb).start()
	response = requests.get(url)
	data = response.json()
	viewers = data["chatters"]["viewers"] + data["chatters"]["moderators"]
	print viewers
	for chatter in viewers:
		if chatter in chatterlist:
			addPoints(chatter)
        	continue
        chatterlist = []
	for chatter in viewers:
		chatterlist.append(chatter)
	print chatterlist
    
def addPoints(chatter):
    sqlAdd = "insert into users(username, points) values(%s, %s)"
    sqlUpdate = "UPDATE users SET points = points + 2 WHERE username=%s", (chatter,)
    cursor.execute("select * from users where username=%s", (chatter,))
    data = cursor.fetchone()
    if data is None:
        cursor.execute(sqlAdd, (chatter, (2)))
    else:
        cursor.execute(*sqlUpdate)
    db.commit()

readWeb()
checkerAPI()