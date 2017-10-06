# NOT FINISHED

import requests
from bs4 import BeautifulSoup

pc = ["acer","dell"]
for i in range(0,2):
    print(pc[i])
    print("")
    url = "https://www.cdiscount.com/search/10/" + pc[i] + ".html#_his_"
    result = requests.get(url)
    html_doc = result.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    for a in range(0,2):
        if (soup.findAll("div", class_="prdtPrSt")[a] != []):
            prixAvant = (soup.findAll("div", class_="prdtPrSt")[a].text).split(',')
            print(prixAvant[0])
            prixApres = (soup.findAll("span", class_="price")[a].text).split('€')
            print(prixApres[0])
            difference = int(prixAvant[0]) - int(prixApres[0])
            print(difference)
        else:
            continue
