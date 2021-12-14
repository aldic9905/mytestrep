from numpy import busday_count
import pyupbit
import telegram
from datetime import date, datetime 
import time
import pandas

def bot_chat(text):   
    bot = telegram.Bot(token='5099900246:AAGdOEWXA4XJ8PBGx234H9YiBOc9v4TcJsE')
    chat_id = 2129243345
    bot.sendMessage(chat_id=chat_id, text=text)

def get_target_price(t,k): 
    df = pyupbit.get_ohlcv(t, interval="minute10", count=2)
    range = df.iloc[0]['high'] - df.iloc[0]['low']
    return df.iloc[1]['open'] + range*k

def get_current_price(t):
    return pyupbit.get_orderbook(ticker=t)["orderbook_units"][0]["ask_price"]

def rsi(ohlc: pandas.DataFrame, period: int = 14):
    delta = ohlc['close'].diff()
    ups, downs = delta.copy(), delta.copy()
    ups[ups < 0] = 0
    downs[downs> 0 ] = 0

    au = ups.ewm(com = period-1, min_periods = period).mean()
    ad = downs.abs().ewm(com = period-1, min_periods = period).mean()
    rs = au/ad

    return pandas.Series(100-(100/(1+rs)), name = "rsi")




access = "yI8stT3XVWVxqlCn4SAuq1aJGqxPBL89oa8QDr9D"          
secret = "UEadUBTIqkz4UfV41alibKxbxVwoojfgYnWa9SvP"          
upbit = pyupbit.Upbit(access, secret)
tick = "KRW-ETH"

btc = upbit.get_balance(tick)  
krw = upbit.get_balance("KRW")
buy_flag = False
sell_flag = False

bot_chat("자동매매 시작")
print("Autotrade Start")
while True:
    try:
        now = datetime.now()
        btc = upbit.get_balance(tick)  
        krw = upbit.get_balance("KRW")
        data = pyupbit.get_ohlcv(ticker="KRW-ETH", interval="minute10")
        now_rsi = rsi(data,14).iloc[-1]

        if now_rsi <= 28 :
            buy_flag = True
        elif now_rsi >= 30 and buy_flag == True :
            upbit.buy_market_order(tick, krw*0.9995)
            buy_flag = False
        elif now_rsi >= 50 :
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
