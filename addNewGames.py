import requests
import json
import includes.helper

def updateNewGame(parameters):
 retryCount= 1
 maxRetry = 5
 timeout = 30
 retry = True
 while retry and retryCount <= maxRetry:
  try:
   shortUrl = "http://gameinfo.online/admin/scrapGames.php"
   response = requests.get(shortUrl,params=parameters,timeout=timeout,allow_redirects=True)
   retry = False
   return response.json()
  except:
   #print(response.text)
   retryCount += 1
         
         
data = {
	           'key' : "811a98-133a27-fc4286-acf829-6599c1",
            "name": "RollerCoaster Tycoon Touch",
            "feature": "Unlimited Money",
            "imgSrc": "https://an1.com/uploads/rollertycoonrvw9qm.png",
            "developer": "Atari, Inc.",
            "version": "3.18.10",
            "os": "Android 4.4",
            "description": "RollerCoaster Tycoon Touch  - continuation of a series of economic and construction simulators in which you will have to build a theme park of attractions. At the same time, your duties will include not only construction itself, but also complete management of the enterprise. In turn, in the RollerCoaster Tycoon Touch mod apk construction will require thoughtful planning, because in all there are more than 240 objects of different directions in the game. In addition, it is necessary to monitor the prestige of the park, its attendance and other aspects.",
            "date": "June 8, 2021",
            "price": "$0",
            "installs": "10 000 000+",
            "size": "396.8Mb",
            "url": "https://an1.com/file_4884-dw.html",
            "category": "Simulations",
            "ratedFor": "3+ years",
            "obb": "https://an1.com/file_4884-dw_cache.html",
            "img": "./images/rollertycoonrvw9qm.png",
            "audio": "./audios/rollertycoonrvw9qm.mp3",
            "processedImage": "./proccessedImages/rollertycoonrvw9qm.png",
            "video": "proccessedVideos/rollertycoonrvw9qm.mp4"
      }
      