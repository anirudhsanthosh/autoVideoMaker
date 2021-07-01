import json
import os
from includes import siteScrap as site
from includes import proccessImage
from includes import proccessVideo
from includes import helper
from includes.helper import color
from includes.helper import jprint
from time import sleep
from tqdm import tqdm
from includes.scrapper import getGameContent
from includes.scrapper import downloadImage
from includes.scrapper import downloadAudio
from includes.tele import sendMessage
from includes.teleMessage import telegram_bot_sendtext



#'\x1b[1K\r', for clear and print on same line


def proccessList(gameList):
 with tqdm(total = len(gameList)) as progress:
  for i in range(len(gameList)):
  
   progress.write(color(f'Proccessing: {gameList[i]}','yellow'))
   gameData = getGameContent( gameList[i] )
   
   progress.write(color('game data loaded \ndownloading image'))
   
   gameData['img'] = downloadImage(gameData['imgSrc'],BASE_IMAGE_DIR,progress.write)
   # if after 5 retries exit the program
   if gameData['img'] is None:
    print(color('unable to download image exiting','red'))
    exit()
   progress.write(color('image downloaded'))
   
   
   """
        get base file name from image name
        and download audio
        
   """
   
   
   baseFileName = gameData['img'].split('ges/')[1].split('.')[0]
   audioFile = BASE_AUDIO_DIR +'/' + baseFileName + '.mp3'
   
   progress.write(color('downloading audiofile','blue'))
   if downloadAudio(gameData['description'],audioFile):
    gameData['audio'] = audioFile
    progress.write(color('audiofile downloaded'))
   else:
    progress.write(color('unable to download audiofile','red'))
    gameData['audio'] = ''
    
   """
        
       proccess image and create template for video
        
   """
   progress.write(color('proccessing image','blue'))
   proccessedData = helper.createTextForImage(gameData)
   gameData['processedImage'] = BASE_PROCCESSED_IMAGE_DIR + '/' + baseFileName + '.png'
   proccessImage.createTemplateImage(gameData['img'],proccessedData,gameData['processedImage'])
   
   progress.write(color('template image created'))
   """
       creating video
       
   """
   progress.write(color('creating video','magenta'))
   gameData['video'] = 'proccessedVideos/' + baseFileName + '.mp4'
   proccessedVideo = proccessVideo .createVideoFromTemplate(gameData['processedImage'],gameData['audio'],VIDEO_DURATION,gameData['video'])
   
   if proccessVideo :
    progress.write(color('video created'))
   
   """
       
       save data to db
       
   """
   
   
   allVideoData = helper.readFile(VIDEO_DB)
   allVideoData.append(gameData)
   helper.saveFile(VIDEO_DB,allVideoData)
   progress.write(color('saved to video db'))
   
   allGameData = helper.readFile(GAME_DB)
   allGameData[ gameList[i] ] = gameData
   helper.saveFile(GAME_DB,allGameData)
   progress.write(color('saved to game db'))
   
   oldlist = helper.readFile(OLD_GAME_LIST)
   oldlist = list(filter(lambda x: x != gameList[i], oldlist))
   oldlist.append(gameList[i])
   helper.saveFile(OLD_GAME_LIST,oldlist)
   progress.write(color('saved to old list'))
   
   
   newGames = helper.readFile(NEW_GAMES)
   newGames.append(gameList[i])
   helper.saveFile(NEW_GAMES,newGames)
   progress.write(color('saved to New_Games.json'))
   
   
   
   progress.write(json.dumps(gameData,indent=4))
   progress.write(color('all items saved'))
   progress.write(color('moving to next game' ,'cyan' ))
   progress.update(1)
   
   helper.toast(str(i+1) +' / ' +str(len(gameList)) + ' completed')
   helper.notifi("video making",str(i+1) +' / ' +str(len(gameList)) + ' completed')





#def proccessList end

# starting of main code

# constants
BASE_URL = 'https://an1.com/tags/MOD/'
PAGE = 'page/'
MAX_NUMBER_OF_GAMES = 15
BASE_IMAGE_DIR = './images'
BASE_AUDIO_DIR = './audios'
BASE_DATA_DIR = './data'
BASE_PROCCESSED_IMAGE_DIR = './proccessedImages'
BASE_PROCCESSED_VIDEO_DIR = './proccessedVideos'
OLD_GAME_LIST = BASE_DATA_DIR + '/oldlist.json'
VIDEO_DB = BASE_DATA_DIR + '/VIDEO_DB.json'
GAME_DB = BASE_DATA_DIR + '/GAME_DB.json'
NEW_GAMES = BASE_DATA_DIR + '/NEW_GAMES.json'
VIDEO_DURATION = 1




# initial url
url = BASE_URL

#verify easch directories
dirs = [
BASE_DATA_DIR,
BASE_IMAGE_DIR,
BASE_AUDIO_DIR,
BASE_PROCCESSED_IMAGE_DIR,
BASE_PROCCESSED_VIDEO_DIR,

]

for dir in dirs:
 if not os.path.exists(dir):
  try:
   dirMakingSuccess = os.mkdir(dir)
   print(color(f'directory {dir} where created','blue'))
  except OSError as error:
   print(f'unable to create directory {dir}')
   print(error)
   exit()

# getting all local data

#loading previous list of games
print(color('fetching old game list','blue'))
filename = OLD_GAME_LIST
oldlist = helper.readFile(filename)

#get all game data
print(color('fetching game data stored locally','blue'))
allGameData = helper.readFile(GAME_DB)

#get all gamelist from an1 index page
print(color('fetching  gameList from an1 index page.....','blue'))
gameList = site.getIndividualGameLinks(url)
print(color('gamelist fetched, number of games loaded: '),len(gameList))

# check previously stored games for last collected game

countOfOldlist = len(oldlist)
print(color('number of games previously recorded is: '),countOfOldlist)


#if oldgamelist is empty download max number of games

if(countOfOldlist == 0):
#make sure we load 15 games atleast
 itrator = 2
 while len(gameList) < MAX_NUMBER_OF_GAMES:
  print(color('number of fetched games are less than limit so loading more games','red'))
  
  newurl = BASE_URL + PAGE + str(itrator) + '/'
  
  newList = site.getIndividualGameLinks(newurl)
  for game in newList:
   gameList.append(game)
   if len(gameList) == MAX_NUMBER_OF_GAMES :
    break
  itrator += 1
 print(color('Games added new games count is '),len(gameList))
 
 # reverse game list for making the the first game last for download it last
 gameList.reverse()
 
 # create videos and save data
 proccessList(gameList)
 os.system('termux-vibrate -d 2000 -f')
 message = f"""
 video making completed
 videos created: {len(gameList)}
 """
 #sendMessage(message)
 telegram_bot_sendtext(message)
else:
 
   """
   
   check last game in oldlist array is in the list or not
   find out the correct previous game
   first reverse the old game list to make the last entry to first
   
   """
   oldlist.reverse()
   LAST_GAME = None 
   for lastgame in oldlist :
    serverData  = getGameContent(lastgame)
    localData = allGameData[lastgame]
    if serverData['version']==localData['version'] :
     LAST_GAME = lastgame
     break
   print('last game found',LAST_GAME)
   """
      now we need to find the games which are uploaded after 
      the last game in our list
   """
   
   if helper.searchInList(gameList,LAST_GAME) == -1:
    # if the last uploaded game is not in the first page list
     #load next page from an1.com untile find that game
     itrator = 2
     loadgames = True
     while loadgames:
      newurl = BASE_URL + PAGE + str(itrator) + '/'
      newList = site.getIndividualGameLinks(newurl)
      gameList.extend(newList)
      if helper.searchInList(gameList,lastgame) != -1:
       loadgames = False
      
      itrator += 1
     
   #modify gamelist slice it
   indexOfLastGame = helper.searchInList(gameList,lastgame)
   gameList = gameList[:indexOfLastGame]
   gameList.reverse()
   if len(gameList) > MAX_NUMBER_OF_GAMES:
    slicingIndex = MAX_NUMBER_OF_GAMES
    gameList = gameList[: slicingIndex]
   
   print('gamelist loaded total games:',len(gameList))
   if len(gameList) == 0:
    print('No new  game found')
    message = f"""
     <b>no new game found</b>
     no new video were created
     """
    #sendMessage(message)
    telegram_bot_sendtext(message)
   else:
    proccessList(gameList)
    os.system('termux-vibrate -d 2000 -f')
    gamelistJoined = '\n\n\n\n'.join(gameList)
    message = f"""
     <b>video making completed</b>
     videos created: {len(gameList)}
     games :
     {gamelistJoined}
     """
    #sendMessage(message)
    telegram_bot_sendtext(message)
   
   

   
   
   
   
   
   
   
   
   
   
   
   
   
   
    
    
     
    
    
     
   
   
 
 
 