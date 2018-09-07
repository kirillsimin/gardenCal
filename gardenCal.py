from bs4 import BeautifulSoup
#from icalendar import Calendar, Event
from dateutil.parser import parse
import urllib
import csv


def parsePage(url):
    req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
    con = urllib.request.urlopen( req )
    content = con.read()
    return BeautifulSoup(content, "lxml")
    
def getVegLinks():
    soup = parsePage("https://hgic.clemson.edu/all-factsheets/")
    links = soup.find_all("a")

    allVegs = []
    
    for link in links:
        if 'HGIC 13' in link.contents[0]:
            allVegs.append(link['href'])
    
    return allVegs

def getVegDates(soup, region):

    if(soup.find("tbody")):
        table = soup.find("tbody")
        rows = table.find_all('tr')
        for row in rows:
            dates = row.findAll('td')
            dates = [date.text.strip() for date in dates]
            if region in dates:
                del dates[0]
                return dates

def parseVeg(url, region='Central'):
    soup = parsePage(url)
    
    title = soup.title.string.split('|')[0]
    
    data = []
    data.append(title)
    data.append(getVegDates(soup, region))    
    return data

def createEvent(vegDates):
    
    try:
        vegetable = vegDates[0]
        dates = []
        if vegDates[1] is list:
            for date in vegDates[1]:
                dates.append(parse(date))
        elif vegDates[1] is not None:
            dates.append(parse(vegDates[1]))
            
        print (dates)
    except:
        print ('could not parse', vegDates[1])
    
#    event = Event()
#    event.add('summary', 'Python meeting about calendaring')
#    event.add('dtstart', datetime(2005,4,4,8,0,0,tzinfo=UTC))
#    event.add('dtend', datetime(2005,4,4,10,0,0,tzinfo=UTC))
#    event.add('dtstamp', datetime(2005,4,4,0,10,0,tzinfo=UTC))
    
#    cal.add_component(event)    

def createCal():
    #cal = Calendar()

    for veg in getVegLinks():
        dates = parseVeg(veg)
        event = createEvent(dates)
        #cal.add_component(event)
    
    return cal.to_ical()


def createList():
    calendar = []
    for veg in getVegLinks():
        parsedVeg = parseVeg(veg)
        name = parsedVeg[0]
        
        if isinstance(parsedVeg[1], list):
            first = parsedVeg[1][0] or ''
            try:
                second = parsedVeg[1][1] or ''
            except:
                second = ''
        else:
            first = parsedVeg[1] or ''
            second = ""

        calendar.append([name, first, second])
    
    return calendar


if __name__ == "__main__":

        
    with open('output.csv', 'w') as myfile:
         wr = csv.writer(myfile)
         wr.writerows(createList())