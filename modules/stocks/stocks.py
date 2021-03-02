import requests
import re
import time
import datetime
token="c0vbedv48v6pqdk9dprg"
regex = r".*[von]\s"

def exec(msg):
    
    name = re.sub(regex, "", msg)
    r = requests.get(f'https://finnhub.io/api/v1/search?q={name}&token='+token).json()
    info = r['result'][0]
    
    ctime = int(time.time() - 900)


    res = requests.get(f'https://finnhub.io/api/v1/stock/candle?symbol={info["symbol"]}&resolution=D&from={ctime}&to={ctime+900}&token='+token).json()
    #res = (finnhub_client.stock_tick(info['symbol'], '2021-03-02', 2, 0))
    price = res['c'][0] * 0.826972742
    
    return { "price": price, "msg": f"Die Aktie {name} steht zur Zeit bei einem Kurs von {price:.3f}€"} 

def init():
    print("Heyho")