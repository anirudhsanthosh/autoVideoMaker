import time
import os
import json
from includes import helper
from includes.helper import jprint
from includes.helper import color
from includes.helper import cprint
from includes import short

#functions

# function for displaying content

def displayItems( gameList = [], gameData = {}, limit = 0):
 start = 1
 length = len( gameList ) 
 for i in range(start,limit) :
  index = length - i
  if index >= 0 :
   cprint(f" {index}. {gameData[ gameList [index]]['name']}",'yellow')


def validateUserInput(data):
 
 if not data.strip().isdigit():
  print("the input",data,'you entered is not a valid integer, type is ',type(data))
  return False
 return True






#initialize
#clearing terminal   
os.system('clear')
start = time.time()



#configuration

limit = 30



# directories

BASE_DATA_DIR = './data'
BASE_PROCCESSED_IMAGE_DIR = './proccessedImages'
BASE_PROCCESSED_VIDEO_DIR = './proccessedVideos'
OLD_GAME_LIST = BASE_DATA_DIR + '/oldlist.json'
VIDEO_DB = BASE_DATA_DIR + '/VIDEO_DB.json'
GAME_DB = BASE_DATA_DIR + '/GAME_DB.json'
NEW_GAMES = BASE_DATA_DIR + '/NEW_GAMES.json'
CONFIG_FILE = BASE_DATA_DIR + '/config.json'
VARIABLES = BASE_DATA_DIR + '/variables.json'

#lastUploadedVideo = helper.readFile(VARIABLES)

filelist = [
{
	"path" : CONFIG_FILE,
	"default" : "{}"
},
{
	"path" : VARIABLES,
	"default" : "{}"
}

]

helper.createNeccesoryFiles(filelist)


exit()
continueUploading = True
i = 1
while continueUploading :
 #clearing terminal   
 os.system('clear')
 #read datas from dbs

 """reading data from OLD_GAME_LIST"""
 oldlist = helper.readFile(OLD_GAME_LIST)
 """ reading GAME_DB """
 gameData  = helper.readFile(GAME_DB)
 
 # Display all games
 cprint("Choose a game from below list: \n","blue")
 displayItems(oldlist,gameData,limit)
 
 retake = True
 while retake:
  # getting user input
  userInput = input(color('\nPlease enter an option from above : \n','cyan'))
  #validating user input
  if validateUserInput(userInput):
    if userInput.isnumeric():
     userInput = int(userInput)
     retake = False
    else:
     cprint("please enter a valid integer","red")
  if not retake and  len(oldlist) <= userInput :
   retake = True
   cprint('please choose an option within the range',"red")
   
  if not retake:
   currentGameUrl = oldlist[userInput]
   gameInfo = gameData[ currentGameUrl ]
   confirmation = input('the game chosen is:\n' + color(json.dumps(  gameInfo,indent=4)) +"\n" + color("continue with this option [y/n]: ", 'blue')) or 'y'
   if confirmation != 'y':
    retake = True
    
 currentVideoIndex = userInput
 continueLooping = True
 while currentVideoIndex < len(oldlist) and continueLooping:
  currentGameUrl = oldlist[currentVideoIndex]
  gameInfo = gameData[ currentGameUrl ]
  print('game loaded: '+ color(gameInfo['name'],"red"),'version: ',color(gameInfo['version'],"red") )
  try:
   gameInfo['obb'] = gameInfo['obb']
  except:
   gameInfo['obb'] = ''
   
  parameters = {
                     'url' : gameInfo['url'],
                     'key' : "811a98-133a27-fc4286-acf829-6599c1",
                     'name' : gameInfo['name'],
                     'img' : gameInfo['imgSrc'],
                     'v' : gameInfo['version'],
                     'u' : gameInfo['date'],
                     'url' : gameInfo['url'],
                     'developer' : gameInfo['developer'],
                     'size' : gameInfo['size'],
                     'obb' : gameInfo['obb'],
              }
 
  cprint('fetching new short url',"blue")
  resultNotOk =True
  shortRetake = 0
  while resultNotOk:
   try :
    newLink = short.fetchShortUrl(parameters)
    resultNotOk = False
   except:
    print('retrying shorting of url, try no: ',shortRetake)
    if shortRetake >= 5 :
     resultNotOk = False
    shortRetake += 1
    time.sleep(10)
 
 
  if newLink['status'] == 'success':
   gameInfo['short'] = newLink['data']['short']
   gameInfo['short1'] = newLink['data']['short1']
  else:
   print('error : ', newLink['errorInfo'])
   exit()
  
  print('new short',gameInfo['short'])
  
  
  
  
  title =f"{gameInfo['name']} MOD APK v {gameInfo['version']}\n\r"
  if not gameInfo['obb'] :
   description = f"""get Apk from: 
 
 1) {gameInfo['short']}
 
 2) {gameInfo['short1']}


{gameInfo['description']}"""
  else:
   description =f"""get Apk and obb from:
1) {gameInfo['short']}

2) {gameInfo['short1']}


{gameInfo['description']}"""
 
  outputVideo = gameInfo['video']
 
  currentVideoIndex +=1
  
   
  #share = "termux-share -d -a send " +outputVideo
  
  
  #sharing directly via termux api binary
  desc = title + '\n' + description
  share = '/data/data/com.termux/files/usr/libexec/termux-api Share --es action send --ez default-receiver true --es title "{0}" --es file "$(realpath {1})"'.format(description ,outputVideo)
  
  
  
  confirmation = input("do you want to share[y/n]: ") or 'y'
  if confirmation != 'y':
     continueLooping = False
  if continueLooping :
   currentVideoIndex += 1
   print('next video: '+ str(	currentVideoIndex))
   
   #commenting old set of code
   # os.system('termux-clipboard-set "' + title+'\n' + description + '"')
   
   os.system('termux-clipboard-set "' + title+ '"')
   print('content copied')
   shareFeedback = os.system(share)
   if shareFeedback == 0:
    #os.system('clear');
    a=1
   else:
    cprint(shareFeedback,'red')
    
   end =time.time()
  
  print('execution duration:' + str( (end - start)/60 ))
 
 confirmation = input("do you wish to upload another video[y/n]: ") or 'y'
 if confirmation != 'y':
    continueUploading = False
end =time.time()
print('execution duration:' + str(  (end - start)/60 ))
 
 
 
 
 
 