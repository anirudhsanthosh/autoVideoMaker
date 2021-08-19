from includes import config
from includes import verifier
from includes import helper
from includes import siteScrap as site
from includes.helper import cprint
from includes.scrapper import getGameContent
from includes.scrapper import downloadImage
from includes.scrapper import downloadAudio
from includes import proccessImage
from includes import proccessVideo
from includes.helper import color
from includes.teleMessage import telegram_bot_sendtext

from tqdm import tqdm

import json
import os

# functions
def proccessList(gameList):
 with tqdm(total = len(gameList)) as progress:
  for i in range(len(gameList)):
  
   progress.write(color(f'Proccessing: {gameList[i]}','yellow'))
   gameData = getGameContent( gameList[i] )
   progress.write(color('game data loaded \ndownloading image'))
   gameData['img'] = downloadImage(gameData['imgSrc'],config.dirs['BASE_IMAGE_DIR'],progress.write)
   # after 5 retries exit the program
   if gameData['img'] is None:
    print(color('unable to download image exiting','red'))
    exit()
   progress.write(color('image downloaded'))
   
   
   """
        get base file name from image name
        and download audio
        
   """
   baseFileName = gameData['img'].split('ges/')[1].split('.')[0]
   audioFile = config.dirs['BASE_AUDIO_DIR']+'/' + baseFileName + '.mp3'
   
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
   gameData['processedImage'] = config.dirs["BASE_PROCCESSED_IMAGE_DIR"] + '/' + baseFileName + '.png'
   proccessImage.createTemplateImage(gameData['img'],proccessedData,gameData['processedImage'])
   
   progress.write(color('template image created'))
   """
       creating video
       
   """
   progress.write(color('creating video','magenta'))
   gameData['video'] = 'proccessedVideos/' + baseFileName + '.mp4'
   proccessedVideo = proccessVideo .createVideoFromTemplate(gameData['processedImage'],gameData['audio'],config.VIDEO_DURATION,gameData['video'])
   
   if proccessVideo :
    progress.write(color('video created'))
   
   """
       
       save data to db
       
   """
   allVideoData = helper.readFile( config.files["VIDEO_DB"] )
   allVideoData.append(gameData)
   helper.saveFile(config.files["VIDEO_DB"],allVideoData)
   progress.write(color('saved to video db'))
   
   allGameData = helper.readFile( config.files["GAME_DB"] )
   allGameData[ gameList[i] ] = gameData
   helper.saveFile(config.files["GAME_DB"],allGameData)
   progress.write(color('saved to game db'))
   
   oldlist = helper.readFile(config.files["OLD_GAME_LIST"])
   oldlist = list(filter(lambda x: x != gameList[i], oldlist))
   oldlist.append(gameList[i])
   helper.saveFile(config.files["OLD_GAME_LIST"],oldlist)
   progress.write(color('saved to old list'))
   
   newGames = helper.readFile(config.files["NEW_GAMES"])
   newGames.append(gameList[i])
   helper.saveFile(config.files["NEW_GAMES"],newGames)
   progress.write(color('saved to New_Games.json'))
   
   progress.write(json.dumps(gameData,indent=4))
   progress.write(color('all items saved'))
   progress.write(color('moving to next game' ,'cyan' ))
   progress.update(1)
   
   helper.toast(str(i+1) +' / ' +str(len(gameList)) + ' completed')
   helper.notifi("video making",str(i+1) +' / ' +str(len(gameList)) + ' completed')
   
#main code

# verify all dirs and files are in place
verifier.verifyDirs(config.dirs)
verifier.verifyFiles(config.files)


# initial url
url = config.BASE_URL

#fetching previously loaded game index
cprint('fetching old game list','blue')
filename = config.files['OLD_GAME_LIST']
oldlist = helper.readFile(filename)

#get all game data
cprint('fetching game data stored locally','blue')
allGameData = helper.readFile(config.files['GAME_DB'])

#create a game list from an1 index page
cprint('fetching  gameList from an1 index page.....','blue')
gameList = site.getIndividualGameLinks(url)
cprint(f"gamelist fetched, number of games loaded: {len(gameList)}")


# check count of previously loaded games to determine which method to be used
countOfOldlist = len(oldlist)

if(countOfOldlist == 0):

#make sure we load 15 games atleast
 itrator = 2
 MAX_NUMBER_OF_GAMES = config.MAX_NUMBER_OF_GAMES
 while len(gameList) < MAX_NUMBER_OF_GAMES:
  cprint('number of fetched games are less than limit so loading more games','red')
  
  newurl = config.BASE_URL + config.PAGE + str(itrator) + '/'
  
  newList = site.getIndividualGameLinks(newurl)
  for game in newList:
   gameList.append(game)
   if len(gameList) == MAX_NUMBER_OF_GAMES :
    break
  itrator += 1
 cprint(f"Games added new games count is {len(gameList)}")
 # reverse game list for making the the first game last for download it last
 gameList.reverse()
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
      newurl = config.BASE_URL + config.PAGE + str(itrator) + '/'
      newList = site.getIndividualGameLinks(newurl)
      gameList.extend(newList)
      if helper.searchInList(gameList,lastgame) != -1:
       loadgames = False
      itrator += 1
      if(itrator == 15):
       
       print("Too many times looped last game is not found ")
       message = f"Too many times looped last game is not found \n last game: {lastgame}"
       telegram_bot_sendtext(message)
       exit()
     #modify gamelist slice it
   indexOfLastGame = helper.searchInList(gameList,lastgame)
   gameList = gameList[:indexOfLastGame]
   gameList.reverse()
   if len(gameList) > config.MAX_NUMBER_OF_GAMES:
    slicingIndex = config.MAX_NUMBER_OF_GAMES
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
   
 
 