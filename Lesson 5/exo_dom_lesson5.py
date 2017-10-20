#Pour le numero de telephone il faut utiliser les api du boncoin

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


url = "https://open-medicaments.fr/api/v1/medicaments?limit=100&query=ibuprofene"
r = requests.get(url)
labels = ['Name','Prix','Annee','Mois']
fichier = []
for i in range(0,100):
    cis = r.json()[i]['codeCIS']
    name = r.json()[i]['denomination']
    url1 = "https://open-medicaments.fr/api/v1/medicaments/" + cis
    r1 = requests.get(url1)
    prix = r1.json()['presentations'][0]['prix']
    date = r1.json()['dateAMM']
    date = date.split('-')
    annee = date[0]
    mois  = date[1]
    fichier.append([name,prix,annee,mois])
df = pd.DataFrame.from_records(fichier, columns=labels)
df.to_csv('ibuprofene.csv')