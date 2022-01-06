import hashlib
import telegram

def bot_chat(text):   
    bot = telegram.Bot(token='5099900246:AAGdOEWXA4XJ8PBGx234H9YiBOc9v4TcJsE')
    chat_id = 2129243345
    bot.sendMessage(chat_id=chat_id, text=text)

a = 'd142afc1ac4a918f459c0a94ca9265ee43841e96'

for i in range(10000000,99999999+1):
    hash = str(i)+'salt_for_you'
    for j in range(500):
        pw = hashlib.sha1(hash.encode()).hexdigest()
    if pw == a :
        bot_chat(str(i)+'salt_for_you')
        break
    if i%100000 == 0 : print(i)
 
