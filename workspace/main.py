import socket, string, oauth
import MySQLdb
import os
# from points import readWeb, addPoints
import requests
import threading
import re
import time

host = "irc.twitch.tv"
nick = "camikazebot"
port = 6667
password = oauth.oauth
channel = "#penquino"
response = ""



s = socket.socket()

s.connect((host, port))

s.send("PASS " + password + "\r\n")
s.send("NICK " + nick + "\r\n")
s.send("JOIN " + channel + "\r\n")

#connect db
db = MySQLdb.connect(os.getenv('IP'), os.getenv('C9_USER'), "", "c9", 3306)
cursor = db.cursor() 

result = ""

last_time = 0
lastsleeptime =0

def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            yield line

def bettingTime():
	global last_time
	curr_time = int(time.time())
	if curr_time - last_time > 50:
		last_time = curr_time
		return False
	else:
		return True

def compareBets(result):
	with open("bets.txt", "r") as betsfile:
		for line in nonblank_lines(betsfile):
			chatter, choice, amount = line.split(" ")[0], line.split(" ")[1], line.split(" ")[2]
			print chatter + " " + choice + " " + amount
			if result == choice:
				amount = amount * 2
				sqlUpdate = "UPDATE users SET points = points + %s WHERE username=%s", (amount, chatter,)
			elif result == "nochange":
				break
			else:
				sqlUpdate = "UPDATE users SET points = points - %s WHERE username=%s", (amount, chatter,)
			cursor.execute(*sqlUpdate)
			db.commit()

def sleep3Secs():
	global lastsleeptime
	curr_time = int(time.time())
	if curr_time - lastsleeptime > 3:
		lastsleeptime = curr_time
		return True
	else:
		return False
			
def getUser(line):
	separate = line.split(":", 2)
	user = separate[1].split("!", 1)[0]
	return user

def getMessage(line):
	separate = line.split(":", 2)
	message = separate[2]
	return message
	
def getCommand(message):
    separate = message.split(" ")
    command = separate[0]
    return command

def chat(s, message):
	if sleep3Secs():
		messageTemp = "PRIVMSG " + channel + " :" + message
		s.send(messageTemp + "\r\n")

   
def getPoints(username):
    cursor.execute("select points from users where username=%s", (username,))
    data = cursor.fetchone();
    print data
    return data

while True:
	response = response + s.recv(1024)
	temp = response.split('\n')
	response = temp.pop()
	for line in temp:
		
	    if "PING" in line:
		    s.send(line.replace("PING", "PONG"))
		    break
		    
        if "PRIVMSG" in line:
    	    user = getUser(line)
    	    msg = getMessage(line)
    	    command = getCommand(msg)
    	    points = getPoints(user)
    	    
    	    print user + ": " + msg
    	    
    	    if '!bet win' in msg or '!bet lose' in msg:
    	    	
    	    	alreadybet = False
    	    	if bettingTime():
    	    		value0 = msg.split(' ')[1]
    	    		try:
    	    			value1 = msg.split(' ')[2]
    	    		except:
    	    			chat(s, "Type !bet win/lose amount")
    	    			break
    	    		
    	    		
    	    		intvalue1 = int(value1)
    	    		print intvalue1
    	    		if (intvalue1 >= points[0]):
    	    			chat(s, "You don't have that many points nerd")
    	    		
    	    		
    	    		if value0 and value1:
    	    			with open("bets.txt", "a+") as myfile:
    	    				for line in myfile:
    	    					if user in line:
    	    						alreadybet = True
	    	    			if alreadybet:
	    	    					chat(s, "U already betted mothafucka!")
	    	    					continue;
		    	    		myfile.write(user + " " + value0 + " " + value1)
    	    			chat(s, user + " betted for " + value0 + " with " + value1)
    	    		else:
    	    			chat(s, "Type !bet win/lose amount")
    	    	else:
    	    		chat(s, "It's not time to bet yet")
    	    
    	  		
    	    if command == 'Hi\r':
    	        chat(s, "Hello")
    	    if command == '!points\r':
    	    	if not points:
    	    		chat(s, "You dont have points yet, wait a little longer.")
    	    	else:
    	    		chat(s, "Points: " + str(points[0]))
    	    
    	    if command == "!result\r":
    	    	if user == "camikazetv" or "penquino" or "nopply":
    	    		if bettingTime():
    	    			chat(s, "Betting is still in progress")
    	    		else:
    	    			with open("results.txt", "r") as resultsfile:
    	    				for line in resultsfile:
    	    					if "win" in line:
    	    						chat(s, "Camikaze has won the game.")
    	    						result = "win"
    	    					elif "nochange" in line:
    	    						chat(s, "No game has been played.")
    	    						result = "nochange"
    	    					else:
    	    						chat(s, "Camikaze has lost the game.")
    	    						result = "lose"
    	    			compareBets(result)
    	    			f = open("bets.txt", 'w')
    	    			f.close()
    	    			r = open("results.txt", 'w')
    	    			r.write("nochange")
    	    			r.close()
    	    			
    	    	else:
    	    		chat(s, "No Authority")
    	    		
    	    if command == '!follow\r':
    	    	chat(s, "Be sure to follow if you haven't already")
    	    if command == '!betnow\r':
    	    	if bettingTime():
    	    		chat(s, "Already been used within 5 mins.")
    	    	else:
	    	    	if user == "camikazetv" or "penquino" or "nopply":
	    	    		bettingTime()
	    	    		if bettingTime():
	    	    			chat(s, "Chat has 5 minutes to bet for the next game!")
	    	    	else:
	    	    		chat(s, "You don't have authority fool.")
	    	    	
    	  		
    	   		