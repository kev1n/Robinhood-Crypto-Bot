from robinhood_crypto_api import RobinhoodCrypto
from bin import pricinginfo
from indicators import ST
import pprint
import time
from multiprocessing import Process
r = RobinhoodCrypto("INSERT GMAIL HERE","INSERT USERNAME HERE")
#Make sure two factor authentication is being sent to your phone
def holdingsinfo(instrument):
    holdings_info = r.holdings()
    pprint.pprint(r.accounts())
    if holdings_info:
        for i in holdings_info:
            for values in i['currency'].values():
                if values == instrument:
                    quantity = float(i['quantity'])
    return quantity
def main(instrument, granularity, multiplier, length, cash):

    listoftime = []
    if instrument == "BTCUSDT":
        name = "Bitcoin"
        rinstru = "BTCUSD"
    if instrument == "ETHUSDT":
        name = "Ethereum"
        rinstru = "ETHUSD"
    print(name)
    while True:
        try:
            time.sleep(0.5)
            times = pricinginfo(instrument = instrument, interval = granularity, number = 5, dfs=0)
            if times not in listoftime:
                listoftime.append(times)
                if len(listoftime) > 1:
                    before, after = ST(instrument = instrument, interval = granularity, number = 100, multiplier=multiplier, length=length)

                    quote_info = (r.quotes(rinstru))['mark_price']

                    quantity = holdingsinfo(name)
                    if quantity == 0:
                        if before == 'SELL' and after == 'BUY':
                            quantities = round(cash/float(quote_info), 5)
                            market_order_info = r.trade(
                                rinstru,
                                price=str(round(float(quote_info) * 1.005, 2)),
                                quantity=str(quantities),
                                side="buy",
                                time_in_force="gtc",
                                type="market"
                            )
                            print('Buy initiated for {}'.format(instrument))
                        
                    else:
                        if before == 'BUY' and after == 'SELL':
                            market_order_info = r.trade(
                                rinstru,
                                price=str(round(float(quote_info) * 0.995, 2)),
                                quantity=str(quantity),
                                side="sell",
                                time_in_force="gtc",
                                type="market"
                            )
                            print('Sell initiated for {}'.format(instrument))
                            
        except Exception as e:
            print(e)
            print('Restarting!')
            time.sleep(30)
            continue

if __name__ == '__main__':
    Process(target=main, args=("BTCUSDT", '1HOUR', 2.9, 13, 34.5)).start()
    time.sleep(10)
    Process(target=main, args=('ETHUSDT', '1HOUR', 2.5, 15, 64.5)).start()

    # process1 = threading.Thread(target = main, args=("BTCUSDT", '1MINUTE', 3, 10, "0.00225"))
    # process2 = threading.Thread(target = main, args=('ETHUSDT', '1MINUTE', 2.5, 15, "0.07"))
    # process1.start()
    # process2.start()

                
        

#ST(instrument = "BTCUSDT", number = 100, interval = "1HOUR", multiplier=3, length=10)
# quote_info = r.quotes()
# market_order_info = r.trade(
#     'BTCUSD',
#     price="5000",
#     quantity="0.000015",
#     side="buy",
#     time_in_force="gtc",
#     type="limit"
# )