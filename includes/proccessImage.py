#Import required Image library
from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageOps
from dropshadow import dropShadow

def createTemplateImage(img,text,output):
 #Create an Image Object from an Image
 im = Image.open(img)
 tempWidth,tempHeight = im.size
 if(tempWidth < 190):
  im = im.resize((190,190))
  tempWidth,tempHeight = (190,190)
  
 templateImage = im.resize((round(tempWidth*2.8),round(tempHeight*2.8)))
 width,height = templateImage.size
 bgWidth = 1280
 bgHeight = 1280
 
 newImage = templateImage.convert('RGBA')
 resized_im = newImage.resize((bgWidth,bgHeight))
 
 
 #blurring background image
 bluredImg = resized_im.filter(ImageFilter.GaussianBlur(90))
 
 
 #cropping background image
 top = 0.25 * bgHeight
 bottom = top +720
 left = 0
 right = bgWidth
 # changing bgHeight to new height
 bgHeight = 720
 bluredImg = bluredImg.crop((left,top,right,bottom))

 
 #adding border to image
 newImage = ImageOps.expand(newImage,border=15,fill='white')
 
 #rounder corner
 
 maskImage = Image.new("RGBA", newImage.size, 0)
 dr = ImageDraw.Draw(maskImage)
 dr.rounded_rectangle(((0,0),newImage.size), radius=15, fill= (255,255,255), outline=None, width=1)

 copyImage = Image.new("RGBA", newImage.size)
 copyImage.paste(newImage, (0,0),maskImage)
 newImage = dropShadow( copyImage,background = (0,0,0,100),shadow = (255,255,255,0), offset = (0,0),border = 20).resize(newImage.size)
 
 
 # rotating image
 angle = 5
 rotatedImage = newImage.rotate(angle,expand=1).resize((width,height))
 
 bluredImg.paste(rotatedImage, (25,15),rotatedImage)
 
 # printing text
 previousWidth = 0
 previousX = 0
 previousX =0
 draw = ImageDraw.Draw(bluredImg)
 
 for printable in text:
  
  if printable['size'] == 'match':
   size = 10
   currentWidth = 0
   currentHeight = 0
   while currentWidth < previousWidth and (currentHeight < printable['maxHeight'] or currentWidth > previousWidth ):
    font = ImageFont.truetype("Teko-Bold.ttf", size= size)
    currentWidth = font.getsize(printable['text'])[0]
    currentHeight = font.getsize(printable['text'])[1]
    size +=1
    
   if previousWidth ==0 : size = printable['fallback']
   printable['size'] = size
   
   #print('cur width: ',currentWidth)
   # print('cur height: ', currentHeight)
   # print('prev width: ', previousWidth)
   # print('falll back: ', printable['maxHeight'])
   # print(currentWidth > previousWidth)
   # 
  
  elif printable['size'] == 'width':
   size = 10
   currentWidth = 0
   currentHeight = 0
   while currentWidth < printable['width'] and currentHeight < printable['maxHeight']:
    font = ImageFont.truetype("Teko-Bold.ttf", size= size)
    currentWidth = font.getsize(printable['text'])[0]
    currentHeight = font.getsize(printable['text'])[1]
    size +=1
    
   if previousWidth ==0 : size = printable['fallback']
   printable['size'] = size
   
  else:
   font = ImageFont.truetype("Teko-Bold.ttf", size= printable['size'])
  
  font_width, font_height = font.getsize(printable['text'])
  new_width = printable['left'] 
  if printable['horizontalCenter'	] : new_width = (bgWidth - font_width)/2
 
  new_height = printable['top']
  if printable['verticalCenter'	] : new_height = (bgHeight - font_height)/2
               
  draw.text((new_width, new_height), printable['text'] , fill=(255, 255, 255),align='center',font=font ,stroke_width=printable['stroke_width'], stroke_fill=(100,100,100,124))
  previousWidth = font_width
  previousX = new_width
  previousY = new_height
  
  if printable['rect'] :
   left = new_width
   top = new_height
   padding = printable['padding']
   
   draw.rounded_rectangle([(left - padding, top +round(font_height * 0.30) - padding ),(left+ font_width +padding, top + font_height +padding)], radius=printable['radius'], fill= printable['fill'], outline= printable['outline'], width=printable['width'])
   
 
 # draw a line at bottom
 #lineTop = round(bluredImg.size[1] * 0.8)
 #draw.line([(0,  lineTop),(bluredImg.size[0],lineTop)], fill= (255,255,255) , width = 4)

 
 bluredImg.save(output)
 
 
 return True
 
 # all the below code is old redundant
 #adding shadow
 #shadowedImage = dropShadow( newImage.convert('RGBA'), offset=(20,20), background=0x000000, shadow=0x000000, border=5, iterations=1)
 shadowedImage = dropShadow( newImage,background = (255,255,255,0),shadow = (0,0,0,155), offset = (0,0))  
 #shadowedImage = shadowedImage.convert('RGBA')
 newImg = Image.new('RGBA',bluredImg.size,(255,255,255,255))
 newImg.paste(shadowedImage, (200,200),shadowedImage)
 newImg.save('newImg'+output)
 shadowedImage.save('shadow'+output)
 
 
 
 
 
 
 
 
 
 
 # rotating image
 angle = 4
 rotatedImage = newImage.rotate(angle,expand=1).resize((width,height))
 rotatedImage.save('newdummy.png')
 maskImage = maskImage.rotate(angle,expand=1).resize((width,height))
 maskImage.save('mask.png')
 
 #bluredImg.paste(templateImage, (round(bgWidth/2 - width/2 ), round(bgHeight/2- height/2)), templateImage.convert('RGBA'))
 bluredImg.paste(rotatedImage, (50,50),maskImage)
 
 
 bluredImg.paste(shadowedImage, (200,200),shadowedImage)

 #bluredImg.show()
 
 
 
 
 
 d1 = ImageDraw.Draw(bluredImg)
 font = ImageFont.truetype("arial.ttf", size=50)
 #printables = ["Hello, TutorialsPoint!","version : 1.2.1.0","author: anirudh"]
 i = 0
 for text in texts:
  printable = text
  font_width, font_height = font.getsize(printable)
  new_width = (bgWidth - font_width) / 2
  new_height = (bgHeight - font_height) / 2 + round(width /4) + i * font_height
  d1.text((new_width, new_height), printable , fill=(255, 255, 255),align='center',font=font ,stroke_width=1, stroke_fill=(100,100,100))
  i +=1
 bluredImg.save(output)
 return True