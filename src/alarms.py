import ccxt


def get_exchanges():
    exchange_list = ccxt.exchanges
    return exchange_list
    

class ExchangeClass:
    def __init__(self, exchange_id):
        self.exchange_id = exchange_id
        exchange_class = getattr(ccxt, self.exchange_id)
        self.exchange = exchange_class(
#        {
#         'apiKey': 'YOUR_API_KEY',
#         'secret': 'YOUR_SECRET',
#         'timeout': 30000,
#         'enableRateLimit': True,  # required! https://github.com/ccxt/ccxt/wiki/Manual#rate-limit
#         }
         )
        self.initialize()
        
    def initialize(self):
        self.exchange.load_markets()
        
    def get_symbols(self):
        symbols = self.exchange.symbols
        return symbols 
    
    def get_current_price(self, pair='BTC/USDT'):
        ticker = self.exchange.fetch_ticker(pair)
        current_price = (float(ticker['ask']) + float(ticker['bid'])) / 2
        return current_price
    
    
    def get_alerts(self, alerts):
        alerts_status = {}
        for pair, alerts_info in alerts.items():
            alerts_status[pair] = []
            current_price = self.get_current_price(pair)
            index = 0
            for i, alert_info in enumerate(alerts_info):
                if (not alert_info['alert_status']) or (alert_info['alert_status'] and alert_info['always']):
                    if alert_info['when'] == 'above': 
                        if current_price > alert_info['alert_price']:
                            alert_status = True
                        else:
                            alert_status = False
                    else:
                        if current_price < alert_info['alert_price']:
                            alert_status = True
                        else:
                            alert_status = False
                            
                    if (not alert_info['alert_status']) or (not alert_status):
                        alerts[pair][index]['alert_status'] = alert_status
                index += 1
               
        return alerts
            

        
    
    
if __name__ == '__main__':
    exchange = ExchangeClass('binance')
    print(exchange.get_current_price('BTC/USDT'))


    alerts = {'BTC/USDT': 
                         [{'alert_price':46500,
                           'when':'above',
                           'always':True,
                           'alert_status': False},
                           {'alert_price':44000,
                           'when':'below',
                           'always':False,
                           'alert_status': False},
                           {'alert_price':43000,
                           'when':'below',
                           'always':False,
                           'alert_status': False}
                           ],
              'SXP/USDT': 
                         [{'alert_price':4,
                           'when':'above',
                           'always':True,
                           'alert_status': False},
                          {'alert_price':3.75,
                           'when':'below',
                           'always':True,
                           'alert_status': False}
                         ]
        }
    
    while True:
        alerts = exchange.get_alerts(alerts)
        
        for pair, alerts_info in alerts.items():
            for alert_info in alerts_info:
                if alert_info['alert_status']:
                    main_currency, stake_currency = pair.split('/')
                    print(f'[ALERT] {main_currency} price is {alert_info["when"]} alert price({alert_info["alert_price"]} {stake_currency})')

    
    
    
