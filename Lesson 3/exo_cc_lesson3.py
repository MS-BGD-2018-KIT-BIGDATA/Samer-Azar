import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

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

<<<<<<< HEAD
def getURLRenaultZoe(ville):
    result_search = []
    url = 'https://www.leboncoin.fr/annonces/offres/' + ville + '?th=1&q=Renault%20Zo%E9&it=1'
    soup = getSoupFromURL(url)
    for s in soup.find_all('li',itemtype="http://schema.org/Offer"):
        regex = r"www.leboncoin.fr/voitures/"
        match = re.search(regex, s.a['href'])
        if match:
            result_search.append(s.a['href'][2:])
    return result_search




villes = ['ile_de_france','aquitaine','provence_alpes_cote_d_azur']
for ville in villes:
    results_search[ville] = getURLRenaultZoe(ville)
    print("----")
    print(ville)
    print("----")
    print(results_search[ville])
=======
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
     
>>>>>>> 2d31a6e72c86bf113c28a5b23d1d9741d60f8900
