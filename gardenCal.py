# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 13:00:22 2016

@author: Kirill
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import csv

def ks():
    print('ks')
    
def getVegs(url="http://www.clemson.edu/extension/hgic/plants/vegetables/crops/"):
    url = urlopen(url)
    content = url.read()
    soup = BeautifulSoup(content)  
    links = soup.find_all("a")
    allVegs = []
    
    for link in links:
        if 'HGIC 13' in str(link):
            allVegs.append(link['href'])
    
    return allVegs
    
def vegInfo(page="hgic1301.html"):
    fullUrl = "http://www.clemson.edu/extension/hgic/"
    fullUrl += "plants/vegetables/crops/"
    fullUrl += page
    webpage = urlopen(fullUrl)
    content = webpage.read()    
    soup = BeautifulSoup(content)
    
    title = soup.title.string
    title = title.strip()
    title = title.split(':',1)[0]
    title = title[10:]
    title = re.sub('\s+', '', title)
    
    data = []
    data.append(title)
    #print('##### &&&& **** ',title)
    
    if(soup.find("tbody")):
        table = soup.find("tbody")        
        rows = table.find_all('tr')        
        for row in rows:
            #print (row)
            cols = row.findAll('td')
            cols = [ele.text.strip() for ele in cols]
            #print(cols)
            #if 'Central' in cols:
            data.append(cols)

    return data

class Vegetable():
     def __init__(self):
        self._piedmont = list()
        self._central = list()
        self._coastal = list()


if __name__ == "__main__":
#==============================================================================
#     print(vegInfo())
#==============================================================================

     allVegs = getVegs()
     for veg in allVegs:
         print()
         print(vegInfo(veg))

