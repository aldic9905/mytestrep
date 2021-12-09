import os
import threading
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
from numpy import e
import requests
import telegram
from datetime import datetime
import time

    
access_key = 'yI8stT3XVWVxqlCn4SAuq1aJGqxPBL89oa8QDr9D'
secret_key = 'UEadUBTIqkz4UfV41alibKxbxVwoojfgYnWa9SvP'
bot = telegram.Bot(token='5099900246:AAGdOEWXA4XJ8PBGx234H9YiBOc9v4TcJsE')
chat_id = 2129243345
#bot.sendMessage(chat_id=chat_id, text="보낼 메세지")
now = datetime.now()

#지갑조회
payld = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payld, secret_key)
authorize_token = 'Bearer {}'.format(jwt_token)
headers = {"Authorization": authorize_token}

res = requests.get("https://api.upbit.com/v1/accounts", headers=headers)

balance = res.json()

#분봉조회
url = "https://api.upbit.com/v1/candles/minutes/10?market=KRW-BTC&count=2"

headers = {"Accept": "application/json"}

response = requests.request("GET", url, headers=headers)

data = response.json()

print("Autotrade Start")
bot.sendMessage(chat_id=chat_id, text="자동매매 시작")
while True:
    bot.sendMessage(chat_id=chat_id, text="매매 재개") 
    print("매매 진행중...")
    flag = 1
    
    if float(balance[0]['balance']) < 5000:
        query = {
            'market': 'KRW-BTC',
            'side': 'ask',
            'volume': balance[1]['balance'],
            'price': data[0]['trade_price'],
            'ord_type': 'limit',
        }
        query_string = urlencode(query).encode()

        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()

        payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
        }

        jwt_token = jwt.encode(payload, secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}
        
        res = requests.post("https://api.upbit.com/v1/orders", params=query, headers=headers) 
        bot.sendMessage(chat_id=chat_id, text="매도완료")
    while (now.minute % 10) < 10 :
        range = float(data[1]['high_price']) - float(data[1]['low_price'])          
        if (float(data[0]['opening_price']) + (range * 0.3)) > float(data[0]['trade_price']) :
            query = {
                'market': 'KRW-BTC',
                'side': 'bid',
                'volume': 0.9995 * float(balance[0]['balance']) / float(data[0]['trade_price']),
                'price': data[0]['trade_price'],
                'ord_type': 'limit',
            }
            query_string = urlencode(query).encode()

            m = hashlib.sha512()
            m.update(query_string)
            query_hash = m.hexdigest()

            payload = {
                'access_key': access_key,
                'nonce': str(uuid.uuid4()),
                'query_hash': query_hash,
                'query_hash_alg': 'SHA512',
            }

            jwt_token = jwt.encode(payload, secret_key)
            authorize_token = 'Bearer {}'.format(jwt_token)
            headers = {"Authorization": authorize_token}
            res = requests.post("https://api.upbit.com/v1/orders", params=query, headers=headers)
            if float(balance[0]['balance'])<5000 and flag == 1:
                time.sleep(10)
                bot.sendMessage(chat_id=chat_id,text="매수완료")
                flag = 0
    time.sleep(1)
print("종료")
bot.sendMessage(chat_id=chat_id, text="종료")  
