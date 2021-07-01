#ffmpeg -loop 1 -i test/pic0001.png -c:v libx264 -t 30 -pix_fmt yuv420p out.mp4

import os
import shlex, subprocess


def createVideoFromTemplate(filename,audio,duration,output):
 
 wd = os.getcwd() + '/'
 filename = wd + filename.replace('./','')
 audio = wd + audio.replace('./','')
 output = wd + output.replace('./','')
 
 # delete existing file
 if os.path.exists(output):
  command = f"rm {output}"
  os.system(command)
 
 """
 command = "ffmpeg -loop 1 -i '{0}' -i '{1}' -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -t {2} '{3}'".format( filename, audio, duration, output)
 

 
 proc = subprocess.Popen(command, stdout=subprocess.PIPE,shell=True, bufsize= 0)
 i = 1
 print(proc)
 while proc.poll() is None:
  line = proc.stdout.readline()
  print(line.strip())
  #print(i)
  #i += 1
 return True

 """

 if audio == '':
  video = os.system("ffmpeg -loop 1 -i {0} -c:v libx264 -t {2} -pix_fmt yuv420p {1}".format(filename,output,duration))
 else: 
  #video = os.system( "ffmpeg -loop 1 -i {0} -i {1} -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -t {2} {3}".format(filename,audio,duration,output) )
  video = os.system("ffmpeg -loop 1 -framerate 18 -i {0} -i {1}  -c:v libx264 -tune stillimage -preset ultrafast -crf 18 -c:a copy -b:a 128k -pix_fmt yuv420p -t {2} {3}".format(filename,audio,duration,output))
 
 if video == 0:
  #print('video created')
  return True
 else:
  return False