
# import libraries
import urllib2
from bs4 import BeautifulSoup
import csv

data = []
spreads = []
predictedTeams = []
teams = []
overUnder = []

def winProb(GameID):
    quote_page = "http://www.espn.com/nba/game?gameId="+str(GameID)

    # getting HTML file
    page = urllib2.urlopen(quote_page)
    soup = BeautifulSoup(page, 'html.parser')

    #get win probability
    #winContainer = soup.find('div', attrs={'id': 'win-probability-container'})
    oddsContainer = soup.find('div', attrs={'class': 'odds-details'})
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



    isNumber = False
    isName = False
    spread = ""
    name = ""
    for i in oddsList:

        if isNumber == True:
            spread += str(i)

        if str(i) == "-":
            isNumber = True
            isName = False


        if str(i) == " ":
            isName = True

        if isName == True:
            name += str(i)


    firstQuaretedSpread = float(spread) / 4
    firstQuaretedOverUnder = float(overUnderValue) / 4

    overUnder.append(firstQuaretedOverUnder)
    spreads.append(firstQuaretedSpread)
    predictedTeams.append("".join(name.split()))

def gameWinner(GameID):

    quote_page = "http://www.espn.com/nba/playbyplay?gameId="+str(GameID)

    # getting HTML file
    page = urllib2.urlopen(quote_page)
    soup = BeautifulSoup(page, 'html.parser')

    # getting scores
    dataTable = soup.find('div', attrs={'id': 'gp-quarter-1'})
    tabel = dataTable.find('table')
    cells = tabel.findAll('tr', attrs={'class': 'scoring-play'})

    #getting teams
    #headerSection = soup.find('div', attrs={'class': 'competitors sm-score'})
    #if headerSection == None:
    #    headerSection = soup.find('div', attrs={'class': 'competitors'})

    #teamNames = headerSection.findAll('span', attrs={'class': 'short-name'})

    miniTable = soup.find('table', attrs={'class': 'miniTable'})
    teamNames = miniTable.findAll('td', attrs={'class': 'team-name'})

    teams = []
    for teamName in teamNames:
        teams.append(teamName.text.strip())


    for cell in cells:
        comboScore = cell.find('td', attrs={'class': 'combined-score'})
        if comboScore != None:
            #data.append(list(score.text.strip()))
            score = list(comboScore.text.strip())
            if float(score[0]) >= 5.0:
                data.append(str(teams[0]))
                break
            elif float(score[4]) >= 5:
                data.append(str(teams[1]))
                break



numberOfGames = 2
gameId = 401071595
for i in range(numberOfGames):
    gameWinner(gameId)
    winProb(gameId)
    print gameId
    gameId -= 1

print spreads
print data
print predictedTeams
print overUnder

for i in range(numberOfGames):
    if data[i] == predictedTeams[i]:
        print "Dog"
    else:
        print "Underdog"



with open('index.csv', 'a') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Team', 'Predicted Team', 'O/U', 'Spread'])
    for i in range(numberOfGames):
        writer.writerow([data[i], predictedTeams[i], overUnder[i], spreads[i]])

csv_file.close()



    #price_box = soup.find('div', attrs={'class':'priceText__1853e8a5'})
    #price = price_box.text
    #print price
