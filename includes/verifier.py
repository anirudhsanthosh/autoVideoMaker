import os
from includes.helper import color

def verifyDirs(dirs):
	for key in dirs:
	 dir = dirs[key]
	 if not os.path.exists(dir):
	  try:
	   dirMakingSuccess = os.mkdir(dir)
	   print(color(f'directory {dir} where created','blue'))
	  except OSError as error:
	   print(f'unable to create directory {dir}')
	   print(error)
	   exit()
	   
def verifyFiles(files):
 for key in files:
  fil = files[key]
  splitPath = os.path.split(fil)
  if not os.path.exists(fil):
   newPath = splitPath[0]
   if not os.path.exists( newPath ):
    try:
     os.makedirs(newPath)
     print("path created",newPath)
    except:
     print("unable to create path",newPath)


 for key in files:
  fil = files[key]
  splitPath = os.path.split(fil)
  ext = os.path.splitext(splitPath[1])[1]
  if not os.path.exists(fil):
   newPath = splitPath[0]
   if os.path.exists( newPath ):
    try:
     f = open(fil,"w")
     if ext == '.json':
      f.write('{}')
     f.close()
     print("file created",fil)
    except:
     print("unable to create file",fil )