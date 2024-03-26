import requests
from Event import Event
from bs4 import BeautifulSoup
from datetime import date
from datetime import timedelta

# Get the current date to make todaysURL
today = date.today()
year = str(today.year)
month = str(today.month)
day = str(today.day)
day_name = today.strftime("%A").lower()

# Pad the month and day with 0s for todaysURL
z_month = str(today.month).zfill(2)
z_day = str(today.day).zfill(2)

# Get yesterdays date to make yesterdaysURL
yesterday = today - timedelta(days=1)
y_year = str(yesterday.year)
y_month = str(yesterday.month)
y_day = str(yesterday.day)
y_day_name = yesterday.strftime("%A").lower()

# Pad the month and day with 0s for the yesterdaysURL
yz_month = str(yesterday.month).zfill(2)
yz_day = str(yesterday.day).zfill(2)

# Build the URLs
baseURL = "https://thotyssey.com/"
todaysURL = (
    baseURL
    + year
    + "/"
    + z_month
    + "/"
    + z_day
    + "/"
    + day_name
    + "-"
    + month
    + "-"
    + day
    + "-"
    + year
    + "/"
)
yesterdaysURL = (
    baseURL
    + y_year
    + "/"
    + yz_month
    + "/"
    + yz_day
    + "/"
    + y_day_name
    + "-"
    + y_month
    + "-"
    + y_day
    + "-"
    + y_year
    + "/"
)

page = requests.get(todaysURL)
# sourceFile = open("page-found.txt", "w")
# print(page.text, file=sourceFile)
# sourceFile.close()

# just for testing so we don't have to keep making requests
# with open("page-found.txt", "r") as file_found:
#    page_found_txt = file_found.read()

# with open("page-not-found.txt", "r") as file_not_found:
#    page_not_found_txt = file_not_found.read()

soup = BeautifulSoup(
    page.content, "html.parser"
)  # use .content (page.content) when you switch

if "page not found" not in soup.title.text.lower():
    print("The page is found!")
    event_date = today
else:
    print("The page is NOT found!")
    page = requests.get(yesterdaysURL)
    soup = BeautifulSoup(page.content, "html.parser")
    event_date = yesterday

# Get all the HTML that is in the "entry-content" class (all the data we want)
entry_content = soup.find("div", class_="entry-content")

# Get all the list items that list out the events going on, without a class (there are some share buttons we want to exclude)
entry_list_items = entry_content.find_all("li", class_="")

# Create list that will store all our events (list of Event objects)
events = []


def populate_events_list():
    for entry_item in entry_list_items:
        # DEBUG: print(index, ": ", entry_item, "\n")
        # works to get venue, but must be a link -> event_venue = entry_item.a.get_text()
        event_text = entry_item.get_text()
        event_venue = event_text[: event_text.find(":")]

        # check if there is more than one event listed
        if ";" not in event_text:
            event_name = event_text[event_text.find(":") + 1 : event_text.find("(")]
            event_time = event_text[event_text.find("(") + 1 : event_text.find(")")]
            events.append(Event(event_venue, event_name, event_time, event_date))
        else:
            multi_event_text = event_text[event_text.find(":") + 1 :]
            event_text_parts = multi_event_text.split(";")
            for i in range(len(event_text_parts)):
                multi_event_part = event_text_parts[i]
                event_name = multi_event_part[: multi_event_part.find("(")]
                event_time = multi_event_part[
                    multi_event_part.find("(") + 1 : multi_event_part.find(")")
                ]
                events.append(Event(event_venue, event_name, event_time, event_date))
                # print(event_text_parts[i].strip())


populate_events_list()

# DEBUG: print(events)
# soup.find(id="title")
# print(results.prettify())
# soup.get_text() gets only the test on the page
