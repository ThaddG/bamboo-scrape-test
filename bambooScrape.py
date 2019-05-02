import requests
from bs4 import BeautifulSoup

result = requests.get("https://www.eventbrite.com/o/bamboo-detroit-5830857275")
src = result.content
soup = BeautifulSoup(src, 'lxml')

times = [] # hold the event times
titles = [] # hold the titles of the events
urls = [] # hold the event links


liveTag = soup.find_all("article", {"id": "live_events"}) #store the live events div
# step inside the live events article
# in the form of a loop to get inside the article but will only loop once
# since there is only one live_events article
for tag in liveTag:
    listCards = tag.find_all("div", {"class": "list-card-v2"}) #store the live cards
    for card in listCards: #iterate through all cards and grab the info from each
        ### TIMES ###
        eventTimes = card.find("time", {"class": "list-card__date"})
        times.append(eventTimes.text)
        ### TITLE ###
        eventTitle = card.find("div", {"class": "list-card__title"})
        titles.append(eventTitle.text)
        ### LINKS ###
        a = card.find('a')
        urls.append(a.attrs['href'])

# uncomment to print the links
# change "urls" to "times" or "titles" to loop through a different list 
#for i in urls:
#    print(i)


#testing comment