import pyupbit
import telegram
from datetime import date, datetime 
import time

def bot_chat(text):   
    bot = telegram.Bot(token='5099900246:AAGdOEWXA4XJ8PBGx234H9YiBOc9v4TcJsE')
    chat_id = 2129243345
    bot.sendMessage(chat_id=chat_id, text=text)

def get_target_price(k): 
    df = pyupbit.get_ohlcv("KRW-BTC", interval="minute10", count=2)
    range = df.iloc[0]['high'] - df.iloc[0]['low']
    return df.iloc[1]['open'] + range*k

def get_current_price(t):
    return pyupbit.get_orderbook(ticker=t)["orderbook_units"][0]["ask_price"]



access = "yI8stT3XVWVxqlCn4SAuq1aJGqxPBL89oa8QDr9D"          
secret = "UEadUBTIqkz4UfV41alibKxbxVwoojfgYnWa9SvP"          
upbit = pyupbit.Upbit(access, secret)


btc = upbit.get_balance("KRW-BTC")  
krw = upbit.get_balance("KRW")

#print(upbit.sell_limit_order("KRW-XRP", 0.00001))
bot_chat("자동매매 시작")
print("Autotrade Start")
while True:
    try:
        now = datetime.now()
        btc = upbit.get_balance("KRW-BTC")  
        krw = upbit.get_balance("KRW")
        
        if (now.minute % 10) < 9 or ((now.minute % 10) == 9 and now.second < 50):
            target_price = get_target_price(0.3)
            current_price = get_current_price("KRW-BTC")
            print(now.second)
            time.sleep(1)
            if(target_price < current_price):
                if(krw > 5000):
                    upbit.buy_market_order("KRW-BTC", krw*0.9995)
                    while True:
                        if(upbit.get_order("KRW-BTC")):
                            print(000000)
                            continue
                        else:
                            bot_chat("매수완료")
                            break
        else:
            if(btc > 0.0008):
                    upbit.sell_market_order("KRW-BTC", btc*0.9995)
                    while True:
                        if(upbit.get_order("KRW-BTC")):
                            print(111111)
                            continue
                        else:
                            bot_chat("매도완료")
                            break
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)



