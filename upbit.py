from numpy import busday_count
import pyupbit
import telegram
from datetime import date, datetime 
import time

def bot_chat(text):   
    bot = telegram.Bot(token='5099900246:AAGdOEWXA4XJ8PBGx234H9YiBOc9v4TcJsE')
    chat_id = 2129243345
    bot.sendMessage(chat_id=chat_id, text=text)

def get_target_price(t,k): 
    df = pyupbit.get_ohlcv(t, interval="minute60", count=2)
    range = df.iloc[0]['high'] - df.iloc[0]['low']
    return df.iloc[1]['open'] + range*k

def get_current_price(t):
    return pyupbit.get_orderbook(ticker=t)["orderbook_units"][0]["ask_price"]



access = "yI8stT3XVWVxqlCn4SAuq1aJGqxPBL89oa8QDr9D"          
secret = "UEadUBTIqkz4UfV41alibKxbxVwoojfgYnWa9SvP"          
upbit = pyupbit.Upbit(access, secret)
tick = "KRW-ETH"

btc = upbit.get_balance(tick)  
krw = upbit.get_balance("KRW")

bot_chat("자동매매 시작")
print("Autotrade Start")
while True:
    try:
        now = datetime.now()
        btc = upbit.get_balance(tick)  
        krw = upbit.get_balance("KRW")
        
        if (now.minute % 60) < 59 or ((now.minute % 60) == 59 and now.second < 55):
            target_price = get_target_price(tick,0.5)
            current_price = get_current_price(tick)
            if(target_price < current_price):
                if(krw > 5000):
                    upbit.buy_market_order(tick, krw*0.9995)
                    while True:
                        if(upbit.get_order(tick)):
                            continue
                        else:
                            bot_chat("매수완료")
                            print("buy")
                            break
        else:
            if(btc > 0.001):
                    upbit.sell_market_order(tick, btc*0.9995)
                    while True:
                        if(upbit.get_order(tick)):
                            continue
                        else:
                            bot_chat("매도완료")
                            print("sell")
                            break
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
