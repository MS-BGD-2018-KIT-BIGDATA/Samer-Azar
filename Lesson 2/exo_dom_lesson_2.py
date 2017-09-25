import requests
from bs4 import BeautifulSoup
import re

for i in range(2010,2016):
    url = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=" + str(i)
    result = requests.get(url)
    html_doc = result.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    print("")
    print(i)
    print("")
    
    # Methode 1 avec css
    res = soup.findAll("td", class_='libellepetit G')
    res1 = soup.findAll("td", class_='montantpetit G')
    h = [r.parent.select_one("td:nth-of-type(2)").text for r in res if re.search('= [ABCD]\Z', r.text)]
    d = dict()
    d[i] = h
         
    for a in range(0,5):
        if a != 2:
            print(res[a].text)
            print("En millier d'Euros : " + res1[3*a].text)
            if (a >= 3):
                print("Euros par habitant : " + d[i][a-1]) # Methode 1
            else:
                print("Euros par habitant : " + d[i][a]) # Methode 1
            print("Euros par habitant : " + res1[1 + 3*a].text) # Methode 2

