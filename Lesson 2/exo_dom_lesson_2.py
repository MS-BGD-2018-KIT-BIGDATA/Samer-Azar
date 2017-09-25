import requests
from bs4 import BeautifulSoup


for i in range(2010,2016):
    url = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=" + str(i)
    result = requests.get(url)
    html_doc = result.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    #soup = soup.select("table:nth-of-type(3)")[0]
    print("")
    print(i)
    print("")
    for a in range(0,5):
        if a != 2:
            print(soup.findAll('td',class_='libellepetit G')[a].text)
            print("En millier d'Euros : " + soup.findAll('td',class_='montantpetit G')[3*a].text)
            print("Euros par habitant : " + soup.findAll('td',class_='montantpetit G')[1 + 3*a].text)
