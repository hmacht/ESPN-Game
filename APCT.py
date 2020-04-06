import urllib2
from bs4 import BeautifulSoup
import csv
import random


def getGameCastSoup(GAMEID):
    # These three lines of code were taken from BeautifulSoup getting started page
    quote_page = "http://www.espn.com/nba/game?gameId="+str(GAMEID)
    page = urllib2.urlopen(quote_page)
    soup = BeautifulSoup(page, 'html.parser')
    return soup

def getStory(GameID):
    story = getGameCastSoup(GameID).find('p', attrs={'class': 'webview-internal'})
    print(story.text.strip())

def getDate(GameID):
    quote_page = "http://www.espn.com/nba/recap?gameId="+str(GameID)
    page = urllib2.urlopen(quote_page)
    soup = BeautifulSoup(page, 'html.parser')

    dateContainer = soup.find('span', attrs={'class': 'timestamp'})
    date = dateContainer.find('span')
    print(date.text)

def getOverUnder(GameID):
    oddsContainer = getGameCastSoup(GameID).find('div', attrs={'class': 'odds-details'})
    percentLabel = oddsContainer.find('li')
    oddsList = list(percentLabel.text.strip())
    overUnderLabel = oddsContainer.find('li', attrs={'class': 'ou'})
    overUnderText = overUnderLabel.text.strip()

    overUnderLabelList = list(overUnderText)
    isOU = False
    overUnderValue = ""
    for i in overUnderLabelList:
        if isOU:
            overUnderValue += str(i)
        if str(i) == " ":
            isOU = True

    return int(overUnderValue)



def getScore(GameID, isName):
    # getting scores
    dataTable = getGameCastSoup(GameID).find('div', attrs={'id': 'gamepackage-linescore-wrap'})
    tabel = dataTable.find('table')
    scores = tabel.findAll('td', attrs={'class': 'final-score'})
    names = tabel.findAll('td', attrs={'class': 'team-name'})
    score1 = int(scores[0].text.strip())
    score2 = int(scores[1].text.strip())

    global combineScore
    combineScore = score1 + score2

    winner = "Team Name"
    if isName == 'TRUE':
        for i in range(2):
            print(names[i].text.strip())

        if score1 > score2:
            winner = names[0]
        else:
            winner = names[1]

        return winner

    else:
        return scores

lives = 3
numberOfGames = 50
gameId = 0
score = 0
alive = True

while alive:
    gameId = random.randint(401071004,401071504)
    getDate(gameId)
    #getScore(gameId, 'TRUE')
    theWinner = getScore(gameId, 'TRUE').text.strip()
    #print(theWinner)
    guess = raw_input("Who Won? ")

    if theWinner == guess.upper():
        print('YES')
        score += 1
    else:
        print('NO')
        bonus = raw_input("Would you like to play the bonus round? ")
        if bonus.upper() == 'NO' or bonus.upper() == 'n':
            lives -= 1
        else:
            overUnder = getOverUnder(gameId)

            guess2 = raw_input("What was the combine score > or < {}? ".format(overUnder))

            if (guess2 == '>') and (combineScore > overUnder) or (guess2 == '<') and (combineScore < overUnder):
                print("Correct, you dont lose any lives")
            else:
                print("Nope, you dnow lose two lives")
                print(combineScore)
                lives -= 2

    print('Score: {}'.format(score))
    print('Lives:')
    for i in range(lives):
        print('*')

    print("Quick Game Recap:")
    getStory(gameId)
    print('----------------------')

    if lives <= 0:
        print("You guessed {0} games correctly").format(score)
        alive = False
