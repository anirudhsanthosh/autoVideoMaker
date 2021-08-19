import requests
from includes import config

def telegram_bot_sendtext(bot_message):
   api_id = '4130401'

   api_hash = '81138a368ac1bd847a7a7e4858c7aaac'

   token = '1873833796:AAGr3Z-kPyI21M-7tetKhhJafWyWXGSPs1Q'


   bot_token = token
   bot_chatID = '@videomaker1234'
   #bot_chatID = '-578810327'
   send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Html&text=' + bot_message
   
   
   response = requests.get(send_text)

   return response.json()