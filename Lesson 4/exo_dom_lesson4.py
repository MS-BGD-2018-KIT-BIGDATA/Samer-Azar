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

def get_nb_pages(url):
    soup = getSoupFromURL(url)
    resultats = soup.find_all("a", {"id": "last"})
    return int(re.sub(r"&brd=Renault&mdl=Zoe", "", resultats[0].get('href'))[-1])

def getURLRenaultZoe(ville):
    result_search = []
    url = 'https://www.leboncoin.fr/voitures/offres/' + ville + '?o=1&brd=Renault&mdl=Zoe'
    nb_pages = get_nb_pages(url)
    for i in range(1, nb_pages+1):
        url_region = 'https://www.leboncoin.fr/voitures/offres/' + ville + '/?o=' + str(i) + '&brd=Renault&mdl=Zoe'
        soup = getSoupFromURL(url_region)
        for s in soup.find_all('li',itemtype="http://schema.org/Offer"):
            result_search.append(s.a['href'][2:])
    return result_search

def getVersion(description):
    zen = re.search('Zen ',description,re.IGNORECASE)
    intens = re.search('Intens ',description,re.IGNORECASE)
    life = re.search('Life ',description,re.IGNORECASE)
    if zen:
        return 'Zen'
    elif intens:
        return 'Intens'
    elif life:
        return 'Life'
    else:
        return 'n/a'
        
def getPrice(soup):
    price = (soup.find_all('span',class_='value')[0].text).strip()
    price = price.split('\xa0')
    nouveauPrix = "" 
    for a in price[0]:
        if a != " ":
            nouveauPrix += a
    nouveauPrix = int(nouveauPrix)
    return nouveauPrix

def getYear(soup):
    year = (soup.find_all('span',class_='value')[4].text).strip()
    return year
    
def getKm(soup):
    km = (soup.find_all('span',class_='value')[5].text).strip()
    km = km.split('KM')
    return km[0]
    
def getProOuPart(soup):
    if soup.find_all(class_="ispro"):
        return 'Professionnel'
    else:
        return 'Particulier'
    
def getPrixArgus(version,annee):
    urlRenaultCote = 'https://www.lacentrale.fr/cote-voitures-renault-zoe--' + annee + '-.html'
    soup = getSoupFromURL(urlRenaultCote)
    if soup:
        all_versions = soup.find_all(class_="listingResultLine")
        if (version == 'Intens'):
            for v in all_versions:
                versionURL = re.search('intens',v.find("a")['href'])
                if versionURL:
                    soup2 = getSoupFromURL("https://www.lacentrale.fr/"+v.find("a")['href'])
                    return soup2.find(class_="jsRefinedQuot").text
        elif (version == "Life"):
            for v in all_versions:
                versionURL = re.search('life',v.find("a")['href'])
                if versionURL:
                    soup2 = getSoupFromURL("https://www.lacentrale.fr/"+v.find("a")['href'])
                    return soup2.find(class_="jsRefinedQuot").text
        elif (version == "Zen"):
            for v in all_versions:
                versionURL = re.search('zen',v.find("a")['href'])
                if versionURL:
                    soup2 = getSoupFromURL("https://www.lacentrale.fr/"+v.find("a")['href'])
                    return soup2.find(class_="jsRefinedQuot").text
        else:
            return ""

def comparaisonPrix(prix,prixArgus):
    nouveauPrix = "" 
    for a in prixArgus:
        if a != " ":
            nouveauPrix += a
    prixArgus = int(nouveauPrix)
    comparaison = prix - prixArgus
    if comparaison > 0:
        return "Plus chère"
    else:
        return "Moins chère"
 
villes = ['ile_de_france','aquitaine','provence_alpes_cote_d_azur']
labels = ['Version','Annee','Prix','Kilometrage','Pro/Part','PrixArgus','Comparaison']
results_search = {}
for ville in villes:
    print('-----')
    print(ville)
    print('-----')
    fichier = []
    results_search[ville] = getURLRenaultZoe(ville)
    for url in results_search[ville]:
        soup = getSoupFromURL("http://" + url)
        description = soup.find_all('p',class_='value')[0].text
        version = getVersion(description)
        annee = getYear(soup)
        prix = getPrice(soup)
        kilometrage = getKm(soup)
        proOuPart = getProOuPart(soup)
        prixArgus = getPrixArgus(version,annee)
        if prixArgus != "":
            comparaison = comparaisonPrix(prix,prixArgus)
        else:
            comparaison = " "
        fichier.append([version,annee,prix,kilometrage,proOuPart,prixArgus,comparaison])
    df = pd.DataFrame.from_records(fichier, columns=labels)
    df.to_csv(ville + '.csv')