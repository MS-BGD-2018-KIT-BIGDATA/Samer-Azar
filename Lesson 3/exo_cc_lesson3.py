# NOT FINISHED 

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def getSoupFromURL(url, method='get', data={}):
    
    if method == 'get':
        res = requests.get(url)
    elif method == 'post':
        res = requests.post(url, data=data)
    else:
        return None
    
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup
    else:
        return None

url = 'https://lespoir.jimdo.com/2015/03/05/classement-des-plus-grandes-villes-de-france-source-insee/'
soup1 = getSoupFromURL(url)
villes = []
for a in range(0,100):
    villes.append((soup1.find_all("td",class_="xl65")[3*a+1].text).strip())
for a in range(0,100):
    print(villes[a])
    for b in range(0,100):
        if (a != b):
            url1 = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + villes[a] + '&destinations=' + villes[b] + '&key=AIzaSyCpXCOmYOUigbPjEvUjmYJdqIWZbFUkpDQ'
            r = requests.get(url1)
            print(r.json()['rows'][0]['elements'][0]['distance']['text'])
            print(villes[b])
     
