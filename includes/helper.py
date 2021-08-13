import json
import os
def createTextForImage(imageData):
 
 proccessedData = []
 #title
 
 proccessedData.append({
           	   'text' : imageData['name'].upper() + 'MOD APK',
           	   'size' : 'width',
           	   'top' : 530,
           	   'left' : 660,
           	   'verticalCenter': False,
           	   'horizontalCenter': True,
           	   'stroke_width' : 2,
           	   'fallback' : 180,
           	   'rect' : False,
           	   'padding' : 20,
           	   'width' : 4,
           	   'outline' : (255,255,255),
           	   'radius' : 20,
           	   'fill' : None,
           	   'width' : 1000,
           	   'maxHeight' : 110
           })
           
 proccessedData.append({
           	   'text' : 'Check description for download link',
           	   'size' : 50,
           	   'top' : 650,
           	   'left' : 660,
           	   'verticalCenter': False,
           	   'horizontalCenter': True,
           	   'stroke_width' : 2,
           	   'fallback' : 180,
           	   'rect' : False,
           	   'padding' : 20,
           	   'width' : 4,
           	   'outline' : (255,255,255),
           	   'radius' : 20,
           	   'fill' : None,
           	   'width' : 1000,
           	   'maxHeight' : 100
           })
 
 #hack
 proccessedData.append({
           	   'text' : 'HACK',
           	   'size' : 210,
           	   'top' : 10,
           	   'left' : 660,
           	   'verticalCenter': False,
           	   'horizontalCenter': False,
           	   'stroke_width' : 3,
           	   'fallback' :230,
           	   'rect' : True,
           	   'padding' : 20,
           	   'width' : 4,
           	   'outline' : (255,255,255),
           	   'radius' : 20,
           	   'fill' : None,
           })
           
 #version
 
 proccessedData.append({
           	   'text' : 'V' + imageData['version'],
           	   'size' : 'match',
           	   'top' : 230,
           	   'left' : 660,
           	   'verticalCenter': False,
           	   'horizontalCenter': False,
           	   'stroke_width' : 3,
           	   'fallback' : 100,
           	   'rect' : True,
           	   'padding' : 20,
           	   'width' : 4,
           	   'outline' : (255,255,255),
           	   'radius' : 20,
           	   'fill' : None,
           	   'maxHeight' : 140
           })
 
 
 
 
  
 proccessedData.append( {
           	   'text' : imageData['size'],
           	   'size' : 90,
           	   'top' : 405,
           	   'left' : 660,
           	   'verticalCenter': False,
           	   'horizontalCenter': False,
           	   'stroke_width' : 2,
           	   'fallback' : 180,
           	   'rect' : True,
           	   'padding' : 20,
           	   'width' : 4,
           	   'outline' : (255,255,255),
           	   'radius' : 20,
           	   'fill' : None,
           })
 
 return proccessedData
 
def jprint(obj):
    # # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text) 
    
def toast(msg):
 os.system('termux-toast '+msg) 
 
def notifi(title,msg):
  os.system("termux-notification --sound -t '"+title+"' -c '"+msg + "' -i 98765")
  
def saveFile(filename,data):
 
 with open(filename, 'w') as outfile:
  json.dump(data,outfile,indent = 6)
  outfile.close()
  
 return True
 
def readFile(filename):
 with open(filename) as json_file:
    text = json_file.read()
    if text != '':
     data = json.loads(text)
    else:
     data = []
    
 return data

def color(txt,color = 'green'):
 
 colors = {
 	
 	  'reset' : 0,
 	  'black' : 30,
 	  'red' : 31,
 	  'green' : 32,
 	  'yellow' : 33,
 	  'blue' : 34,
 	  'magenta' : 35,
 	  'cyan' : 36,
 	  'white' : 37
 }
 
 #start = f'\e[1;{colors[color]}m'
 # end = '\e[0m'
 
 start = f'\033[0;{colors[color]}m'
 end = '\033[0m'
 
 return start + str(txt) + end
 
def cprint(txt= '',color = 'green'):
 
 colors = {
 	
 	  'reset' : 0,
 	  'black' : 30,
 	  'red' : 31,
 	  'green' : 32,
 	  'yellow' : 33,
 	  'blue' : 34,
 	  'magenta' : 35,
 	  'cyan' : 36,
 	  'white' : 37
 }
 
 #start = f'\e[1;{colors[color]}m'
 # end = '\e[0m'
 
 start = f'\033[0;{colors[color]}m'
 end = '\033[0m'
 
 print(start + str(txt) + end)
 
 
def searchInList(array =[],search = ''):
 
 if search in array:
  return array.index(search)
 else:
  return -1
  
def createNeccesoryFiles(files = []):
 for fileToCreate in files:
  fil = fileToCreate["path"]
  if not os.path.exists(fil):
   newPath = os.path.split(fil)[0]
   if not os.path.exists( newPath ):
    try:
     os.makedirs(newPath)
     print("path created",newPath)
    except:
     print("unable to create path",newPath)
 
 for fileToCreate in files:
  fil = fileToCreate["path"]
  if not os.path.exists(fil):
   newPath = os.path.split(fil)[0]
   if os.path.exists( newPath ):
    try:
     f = open(fil,"w")
     f.write(fileToCreate["default"])
     f.close()
     print("file created",fil)
    except:
     print("unable to create file",fil )