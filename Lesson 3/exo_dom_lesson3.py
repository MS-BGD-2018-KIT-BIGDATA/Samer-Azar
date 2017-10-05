import requests
from bs4 import BeautifulSoup
import pandas as pd
from multiprocessing import Pool

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

def getTopContributors(url):
    soup = getSoupFromURL(url)
    topContributors = []
    for cell in soup.find_all("th", scope='row'):
        print(cell.parent.th.text + ' ' + cell.parent.a.text)
        topContributors.append(cell.parent.a.text)
    return topContributors

def getUserRepAvgStars(user):
    url = 'https://api.github.com/users/' + user + '/repos'
    r = requests.get(url) #auth=(username,password)
    if r.status_code == 200:
        mean = pd.Series([rep['stargazers_count'] for rep in r.json()]).mean()
        return round(mean,3)
    else:
        return 'url wrong response'

if __name__ == '__main__':
    url = 'https://gist.github.com/paulmillr/2657075'
    topUsers = getTopContributors(url)
    # p = Pool(5)
    # print(topUsers,p.map(getUserRepAvgStars,topUsers))
    for user in topUsers:
        print(user,getUserRepAvgStars(user))