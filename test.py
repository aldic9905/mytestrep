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
tick = ["KRW-ETH", "KRW-BTC", "KRW-XRP", "KRW-SAND","KRW-DOGE"]
pre_rsi = [-1,-1,-1,-1,-1]
buy_flag = [-1,-1,-1,-1,-1]
sell_flag = [-1,-1,-1,-1,-1]
bot_chat("자동매매 시작")
print("Autotrade Start")
while True:
    try:
        now = datetime.now()
        krw = upbit.get_balance("KRW")
        
        for i in range(len(tick)):
            btc = upbit.get_balance(tick[i])
            data = pyupbit.get_ohlcv(ticker=tick[i], interval="minute30")
            now_rsi = rsi(data,14).iloc[-1]
            if now_rsi > pre_rsi and pre_rsi != -1:
                sell_flag[i] = 0
            elif now_rsi < pre_rsi and sell_flag==0 and pre_rsi != -1:
                if btc:
                    upbit.sell_market_order(tick[i], btc)
                    while True:
                        if(upbit.get_order(tick[i])):
                            continue
                        else:
                            bot_chat(tick[i]+" 매도완료")
                            print("sell")
                            break
                sell_flag[i] =-1
            if now_rsi < pre_rsi and pre_rsi != -1:
                buy_flag[i] = 1
            elif now_rsi > pre_rsi and buy_flag==1 and pre_rsi != -1:
                if krw > 5000:
                    upbit.buy_market_order(tick[i], krw*0.9995)
                    while True:
                        if(upbit.get_order(tick[i])):
                            continue
                        else:
                            bot_chat(tick[i]+" 매수완료")
                            print("buy")
                            break
                buy_flag[i] =-1
        pre_rsi = rsi(data,14).iloc[-1]
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
