import requests
from bs4 import BeautifulSoup

def getIndividualGameLinks(href):
 retryCount= 1
 maxRetry = 5
 timeout = 30
 retry = True
 
 while retry and retryCount <= maxRetry:
  try:
   game = requests.get(href,timeout=timeout)
   retry = False
  except:
   print('retrying to gather game data, try no:',retryCount)
   retryCount += 1
   
 soup = BeautifulSoup(game.content, 'html.parser')
 items = soup.findAll(class_='name')
 games = []
 for item in items:
  games.append(item.find('a')['href'])
 return games
 