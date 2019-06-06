from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

from datetime import datetime, timedelta
import datefinder
import requests
import calendar
from bs4 import BeautifulSoup


"""======================================
  SCRAPED INFO
======================================"""
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
"""======================================
  SCRAPED INFO
======================================"""

scopes = ['https://www.googleapis.com/auth/calendar']
flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)
# not needed after first run
# make a check to see if there isnt credentials yet
# maybe if credentials == None
credentials = flow.run_console()
# dump the credentials obj that holds the credentials into a pickle file
pickle.dump(credentials, open("token.pkl", "wb"))
# load the credentials so it doesnt have to request permission again
# this will most likely need an if statement
credentials = pickle.load(open("token.pkl", "rb"))
# build the calendar api
service = build("calendar", "v3", credentials=credentials)

calendarResult = service.calendarList().list().execute()
calendar_id = calendarResult['items'][0]['id']
calendarResult = service.events().list(calendarId=calendar_id).execute()

timezone = 'America/Detroit'
def create_event(start_time_str, summary, duration=1, description=None, location=None):
      matches = list(datefinder.find_dates(start_time_str))
      if len(matches):
            start_time = matches[0]
            end_time = start_time + timedelta(hours=duration)
      
      event = {
          'summary': summary,
          'location': location,
          'description': description,
          'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
          },
          'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
          },
          'reminders': {
            'useDefault': False,
            'overrides': [
              {'method': 'email', 'minutes': 24 * 60},
              {'method': 'popup', 'minutes': 10},
            ],
          },
        }
      return service.events().insert(calendarId='primary', body=event).execute()


# create_event("9 june 6 PM", "Test Using Function")