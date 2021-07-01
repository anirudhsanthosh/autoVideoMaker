import requests
from bs4 import BeautifulSoup

from urllib.parse import urlparse
import os
import time
from gtts import gTTS


#get game content
def getGameContent(href):
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
 data = {}
 data['name'] = soup.find( 'h1', itemprop="name").text
 data['name'] = data['name'].split('Download')[1]
 data['name'] = data['name'].split('(')[0].strip()
 
 data['feature'] = soup.find( 'h1', itemprop="name").text.split('(')[1]
 data['feature'] = data['feature'].split(')')[0]
 data['feature'] = data['feature'].split('MOD')[1].strip()
 if data['feature'].find(',') == 0:
  data['feature'] = data['feature'].split(',')[1].strip()
 
 imageSrc = soup.find(class_='app_view-first').find('img')['src']
 data['imgSrc'] =imageSrc
 
 
 data['developer'] = soup.find(class_='developer').find('span').text
 
 data['version'] = soup.find(class_='spec').find(itemprop="softwareVersion").text
 
 data['os'] = soup.find(class_='spec').find(itemprop="operatingSystem").text
 
 
 description = soup.find( itemprop="description" ).text
 
 description = description.split('(')[0] + description.split(')')[1];
 
 data['description'] = description
 
 data['date'] = soup.find(itemprop="datePublished").text
 
 data['price'] = soup.find(itemprop="price").text
 
 data['installs'] = soup.find(itemprop="datePublished").text
 
 data['size'] = soup.find(itemprop="fileSize").text
 
 data['url'] = "https://an1.com" +soup.find(class_="download_line")['href']
 
 data['category'] = soup.find(itemprop='applicationSubCategory').text
 
 data['installs'] = soup.findAll(class_='spec')[1].findAll('li')[2].text.split('Installs')[1].strip()

 data['ratedFor'] = soup.findAll(class_='spec')[1].findAll('li')[3].text.split('for')[1].strip()
 
 
 # checking for obb
 files = soup.find_all('a', "download_line")
 
 if len(files) > 1 :
  validationStr = files[0]['href'].split('.')[0]+"_cache.html"
  if validationStr == files[1]['href'] :
   data['obb'] = "https://an1.com" + files[1]['href']
  else:
   data['obb'] = False
 else:
  data['obb'] = False
 return data
 



 

#download images from an1
def downloadImage(url,base,tprint):
 #now = datetime.now()
 #newFileName= str( math.floor(datetime.timestamp(now)))
 
 dirOk = True;
 if not os.path.exists(base):
   dirMakingSuccess = os.mkdir(base)
   if dirMakingSuccess == 0:
    print(f'directory {base} where created')
   else:
    print(f'unable to create directory {base}')
    dirOk= False
 if dirOk:
 
  retryCount= 1
  maxRetry = 5
  timeout = 30
  retry = True
  while retry and retryCount <= maxRetry:
   try:
    imageData = requests.get(url,timeout=timeout,allow_redirects=True)
    retry = False
   except:
    tprint('retrying to download image, try no:{retryCount}')
    retryCount += 1
 
  #after downloading save the image
  pathOfImage = urlparse(url).path
  newFilePath = base+'/'+os.path.basename(pathOfImage)
  imageRetrived = open(newFilePath,'wb').write(imageData.content)
  # if image is downloaded imageRetrived will be total size
  if imageRetrived :
   return newFilePath
  else:
    return None
 
 # download audio from text
def downloadAudio(txt,filename):
 retryDownloadAudio = True
 downloadFaild = True
 retryCount = 0
 while retryDownloadAudio :
  try:
   tts = gTTS(txt, lang='en')
   tts.save(filename)
   retryDownloadAudio = False
   downloadFaild = False
   return True
  except :
   if retryCount < 5:
    retryDownloadAudio = True
   else:
    retryDownloadAudio = False
    return False
   retryCount += 1
   time.sleep(2)
 
 
 