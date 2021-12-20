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
tick = ["KRW-ETH", "KRW-BTC", "KRW-SOL", "KRW-SAND","KRW-MATIC"]
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
            if now_rsi <= 32 :
                if krw > 5000:
                    upbit.buy_market_order(tick[i], krw*0.9995)
                    while True:
                        if(upbit.get_order(tick[i])):
                            continue
                        else:
                            bot_chat(tick[i]+" 매수완료")
                            print("buy")
                            break
            elif now_rsi >= 60 :
                if btc:
                    upbit.sell_market_order(tick[i], btc)
                    while True:
                        if(upbit.get_order(tick[i])):
                            continue
                        else:
                            bot_chat(tick[i]+" 매도완료")
                            print("sell")
                            break
        time.sleep(1)
    except Exception as e:
        print(e)
        bot_chat("ERROR")
        break;
        time.sleep(1)
bot_chat("SERVER DOWN")
