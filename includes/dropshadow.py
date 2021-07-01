
from PIL import Image, ImageFilter, ImageOps

def dropShadow( image, offset=(0,0), background=0xffffff, shadow=0x444444, 
                border=8,blurRadius=5):
  
  
  # Create the backdrop image -- a box in the background colour with a 
  # shadow on it.
  totalWidth = image.size[0] + abs(offset[0]) + 2*border
  totalHeight = image.size[1] + abs(offset[1]) + 2*border
  back = Image.new(image.mode, (totalWidth, totalHeight), background)
  
  imwidth,imheight = image.size
  margin= border
  
  # creating a mask in the shape of input image
  imageMask = Image.new('RGBA',image.size,(0,0,0,0))
  imageMask.paste((255,255,255),[0,0,imwidth,imheight],image)
  
  #creating a blurred image mask based on previous mask
  backBlur = Image.new('L',back.size,0)
  backBlur.paste(255,[margin,margin,back.size[0]-margin,back.size[1]-margin],imageMask)
  backBlur = backBlur.filter(ImageFilter.GaussianBlur(blurRadius))
  
  width,height = backBlur.size
  backBlur.paste(imageMask.convert('L'),
                  (round((width-imwidth)/2),round((height-imheight)/2)),
                  imageMask.convert('L'))
  
  baseImage = Image.new(back.mode,back.size)
  secondBaseImage = baseImage.copy()
  result = baseImage.copy()
  baseImage = Image.alpha_composite(baseImage,back)
  secondBaseImage.paste(image,(border, border),imageMask)
  baseImage = Image.alpha_composite(baseImage,secondBaseImage)
  result.paste(baseImage,(0,0),backBlur)
  return result