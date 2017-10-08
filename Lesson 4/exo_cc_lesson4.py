# 25% DONE

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
