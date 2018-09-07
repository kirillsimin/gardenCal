from bs4 import BeautifulSoup
import urllib


def parsePage(url):
    req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
    con = urllib.request.urlopen( req )
    content = con.read()
    return BeautifulSoup(content)
    
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
                return dates

def parseVeg(url, region='Central'):
    soup = parsePage(url)
    
    title = soup.title.string.split('|')[0]
    
    data = []
    data.append(title)
    data.append(getVegDates(soup, region))    

    return data


if __name__ == "__main__":

    allVegs = getVegLinks()
    for veg in allVegs:
        print(parseVeg(veg))


