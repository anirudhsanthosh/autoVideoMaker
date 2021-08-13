import os
import json
from datetime import date


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


"""
initiallize variables
"""
dataFile = "report_storage.json"
messages = [
"""please choose an option
 1. add report [default]
 2. add field
 3. copy data
""",

]


today = date.today()

# dd/mm/YY
todayDate = today.strftime("%d/%m/%Y")
# questions for setting up optiins

questions = [

 {
 	 'text' : 'title',
 	 'name' : 'title',
 	 'type' : 'text',
 	 'default' : None
 },
 {
 	 'text' : 'persistance [y/n default: False]',
 	 'name' : 'persistance',
 	 'type' : 'boolian',
 	 'default' : False
 },
 {
 	 'text' : 'add up name',
 	 'name' : 'addUpName',
 	 'type' : 'text',
 	 'default' : None
 },
 {
 	 'text' : 'value',
 	 'name' : 'value',
 	 'type' : 'text',
 	 'default' : None
 },
 
 {
 	 'text' : 'sum',
 	 'name' : 'sum',
 	 'type' : 'number',
 	 'default' : 0
 },
 
]

savedFileds = []

"""
 initialize files
"""
if not os.path.exists(dataFile):
 print('file not found')
 f = open(dataFile,'a')
 f.write("[]")
 f.close
 savedFileds = []
else:
 f = open(dataFile,'r')
 savedFileds = json.load(	f)
 f.close()
 

"""
initiate app
"""
os.system('clear')
cprint(messages[0],"blue")
choice = input("Enter option: ") or "2"
choice = int(choice)
print(choice)
if choice >3 or choice < 1:
 print('choice not found')
 exit()
 
if choice == 1:
 for field in savedFileds:
  error = True
  while error :
   value = input(f"{field['title']} :\n[old value: {field['value']}] \nNew value: ") or field['value']
   if field['addUpName'] != None:
    try:
     value = int(value)
     error = False
    except:
     print('value should be a number')
   else:
    error = False
    
    
  field['value']= value
  if field['addUpName'] != None:
   if field['value'] != None:
    field['sum'] += value
   else:
    field['sum'] = value
 f= open(dataFile,"w")
 json.dump(savedFileds,f,indent=4)
 
 template = []
 
 for data in savedFileds:
  template.append(f"{data['title']} : {data['value']} ")
  if data['addUpName'] != None:
   template.append(f"{data['addUpName']} : {data['sum']}")

 os.system('clear')
 #todayDate
 joint = '\n'
 joint = joint.join(template)
 
 
 basicTemplate = f"""Store name: *Lulu fashionstore*  
Date: {todayDate}
{joint}"""
 print(basicTemplate)
 confirmation = input('share this...?') or 'y'
 if confirmation == 'y':
  os.system(f'termux-clipboard-set "{basicTemplate}"')
  print('copied to clipboard')
  
 else:
  exit()
 
 
 
 
if choice == 2 :
 newFields = []
 addMore = True
 while(addMore):
  template = {}
  for question in questions:
   template[question['name']] = input(f"{question['text']}: ") or question['default']
  print(json.dumps(template,indent = 4))
  newFields.append(template)
  wantToAddMore = input('Do you want to add more? [y/n] ')  or 'y'
  if wantToAddMore != "y":
   addMore = False
 print(json.dumps(newFields,indent = 4))
 savedFileds.extend(newFields)
 f= open(dataFile,"w")
 json.dump(savedFileds,f,indent=4)
 
if choice == 3 :
 template = []
 
 for data in savedFileds:
  template.append(f"{data['title']} : {data['value']} ")
  if data['addUpName'] != None:
   template.append(f"{data['addUpName']} : {data['sum']}")

 os.system('clear')
 #todayDate
 joint = '\n'
 joint = joint.join(template)
 
 
 basicTemplate = f"""Store name: *Lulu fashionstore*  
Date: {todayDate}
{joint}"""
 print(basicTemplate)
 confirmation = input('share this...?') or 'y'
 if confirmation == 'y':
  os.system(f'termux-clipboard-set "{basicTemplate}"')
  print('copied to clipboard')