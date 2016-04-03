import requests
import threading
import re

oldMatchesPlayed = 0
oldMatchesWon = 0
oldMatchesLost = 0
# matchesPlayed = 0
# matchesWon = 0
# matchesLost =0

def readAPI():
    global oldMatchesPlayed
    global oldMatchesWon
    global oldMatchesLost
    nochange = False
    # global MatchesPlayed
    # global MatchesWon
    # global MatchesLost
    url = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key=8592039D12A3474A6CEAF70F572401EB&steamid=76561197984713986"
    r = requests.get(url)
    data = r.json()
    matchesPlayed = data["playerstats"]["stats"][126]['value'] #Static Values in array
    matchesWon = data["playerstats"]["stats"][127]['value'] 
    matchesLost = matchesPlayed - matchesWon
    won = checkGame(matchesPlayed, matchesWon, matchesLost, oldMatchesPlayed, oldMatchesLost, oldMatchesWon)
    if won:
        print "won"
    else:
        if matchesPlayed == oldMatchesPlayed:
          nochange = True
          print "no change"
        else:
          print "lost"
    with open("results.txt", "w") as myfile:
        if won:
          myfile.write("won")
        else:
          if nochange:
            myfile.write("nochange")
          else:
            myfile.write("loss")
          
    
    oldMatchesPlayed = matchesPlayed
    oldMatchesWon = matchesWon
    oldMatchesLost = matchesLost
    

def checkGame(matchesPlayed, matchesWon, matchesLost, oldMatchesPlayed, oldMatchesLost, oldMatchesWon):
    # global oldMatchesPlayed
    # global oldMatchesWon
    # global oldMatchesLost
    # global matchesWon
    # global matchesPlayed
    # global matchesLost
    if matchesPlayed - oldMatchesPlayed == 1:
        if matchesWon - oldMatchesWon == 1:
            return True
        elif oldMatchesLost - matchesLost == 1:
            return False
readAPI()