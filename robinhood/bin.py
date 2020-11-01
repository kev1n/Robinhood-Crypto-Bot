from binance.client import Client
import pprint
import pandas as pd

def pricinginfo(instrument, interval, number, dfs):
    api_key = "VRGdRhQjQapEUu0jIivAlg47kBIxvYmWYZ0JC4g5sU6fCiE6hnbH9MaPSddKyYcL"
    api_secret = "Hxd8qoGPXvSmzZJWzJRHcK6MJeftFW925BIjkR5bpDv57JckTyU6jFZQKXe01Act"

    client = Client(api_key, api_secret)

    klines = client.get_historical_klines(instrument, eval("Client.KLINE_INTERVAL_{}".format(interval)), "{} hours ago EST".format(number))
    klines.pop()
    if dfs == 1:
        t = []
        o = []
        h = []
        l = []
        c = []
        v = []
        
        for i in klines:
            t.append(i[0])
            o.append(float(i[1]))
            h.append(float(i[2]))
            l.append(float(i[3]))
            c.append(float(i[4]))
            v.append(float(i[5]))


        data = {
            'Open': o,
            'High': h,
            'Low': l,
            'Close': c,
            'Volume': v,
        }
        df = pd.DataFrame(data=data, columns=['Open', 'High', 'Low', 'Close', 'Volume'])
        return df, t
    if dfs == 0:
        return klines[0][0]

