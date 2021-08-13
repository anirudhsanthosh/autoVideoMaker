import requests
import json
from includes import helper

def fetchShortUrl(parameters):
 try:
  shortUrl = "http://gameinfo.online/admin/short.php"
  response = requests.get(shortUrl,params=parameters)
  #print(response.content)
  return response.json()
 except:
  print(response.text)
  return {
  	         "status" : 'error',
  	         "errorInfo" : 'couldnt fetch data'
         }