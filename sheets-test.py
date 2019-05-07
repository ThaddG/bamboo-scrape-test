import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

import requests
from bs4 import BeautifulSoup

"""====================
    SCRAPED INFORMATION
===================="""

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

"""===========================
    END OF SCRAPED INFORMATION
==========================="""

scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
# replace the json file with personal credentials file
creds = ServiceAccountCredentials.from_json_keyfile_name("test-sheets-creds.json", scope)
client = gspread.authorize(creds)
# replace "test-sheet" with personal google sheet file
sheet = client.open("test-sheet").sheet1
data = sheet.get_all_records()

# PUTTING INFO INTO SHEETS
sheet.insert_row(titles, 1)
sheet.insert_row(times, 2)
sheet.insert_row(urls, 3)