import os
import time
import json
import streamlit as st
import pandas as pd

import rerun

from threading import Thread

from backend import check_alert_status
from alarms import ExchangeClass, get_exchanges



def choose_pair(exchange):
    symbols = exchange.get_symbols()
    pair = st.sidebar.selectbox("Choose a Pair", symbols)
    return pair 

def get_alert_params(pair):    
    with st.sidebar.form(key ='Form1'):
        alert_price =  st.number_input(f"Enter alert price:")
        when = st.selectbox("Show alarm when the price is:",['above', 'below'])
        always = st.checkbox('always')
        add_alert_button = st.form_submit_button(label = f'Add alert for {pair}')
    
    return alert_price, when, always, add_alert_button

def create_alerts(exchange_id, pair, alert_price, when, always, alerts=None):
    if alerts is None:
        alerts = {}
        
    alert_info = {'alert_price':alert_price,
                  'when':when,
                  'always':always,
                  'exchange':exchange_id,
                  'alert_status': False}
    
    if len(alerts) and pair in alerts.keys():
        if alert_info in alerts[pair]:
            print("It is already added!")
        else:
            alerts[pair].append(alert_info)
    else:
        alerts[pair] = [alert_info]
    return alerts

def get_df(alerts):
    exchange_list = []
    pair_list = []
    when_list = []
    alert_price_list = []
    frequency_list = []
    alert_status_list = []
    for pair, alerts_info in alerts.items():
        for alert_info in alerts_info:
            exchange_list.append(alert_info['exchange'])
            pair_list.append(pair)
            alert_price_list.append(alert_info['alert_price'])
            when_list.append(alert_info['when'])
            if alert_info['always']:
                frequency = 'always'
            else:
                frequency = 'once'
            frequency_list.append(frequency)
            alert_status_list.append(alert_info['alert_status'])
    
    df = pd.DataFrame({"Exchange":exchange_list, "Pairs": pair_list, 
                       "Alert Price": alert_price_list, "When": when_list,
                       "Frequency": frequency_list, "Alert": alert_status_list})
    return df
    

def check_price(exchange, alerts):
    previous_alerts = alerts
    while True:
        time.sleep(5)
        alerts = exchange.get_alerts(alerts)
        
        if (alerts != previous_alerts):
            return alerts
            
        
        
def main_ui():
    save_dir = '../cfg/'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        
    df = None
    
    if not os.path.exists(f'{save_dir}alerts.json'):
        alerts = {}
    else:
        with open(f'{save_dir}alerts.json') as json_file:
            alerts = json.load(json_file)
    
    df = get_df(alerts)
    
    st.title("Cryptocurrency Price Alerts")
    
#    exchange_list = get_exchanges()
    exchange_list = ["binance"]
    exchange_id = st.sidebar.selectbox("Choose an Exchange", exchange_list, index=exchange_list.index('binance'))
    exchange = ExchangeClass(exchange_id)
    symbols = exchange.get_symbols()
    
    pair = st.sidebar.selectbox("Choose a Pair", symbols, index=symbols.index('BTC/USDT'))

    current_price = exchange.get_current_price(pair)   
    
    st.sidebar.write(f"Current Price for {pair} : {current_price}")
    
    alert_price, when, always, add_alert_button = get_alert_params(pair)
    
    if add_alert_button:
        alerts = create_alerts(exchange_id, pair, alert_price, when, always, alerts)

        df = get_df(alerts)
        with open(f'{save_dir}alerts.json', 'w') as outfile:
            json.dump(alerts, outfile)

    st.table(df)

    
    st.markdown('''<html lang="en">
<body>
    
  	<div>
  		<p>Designed by <em><a href="https://github.com/sefaburakokcu/">Sefa Burak OKCU</a></em></p> 
	</div>
</body>
</html>''', unsafe_allow_html=True)
    
    
#    time.sleep(10)
#    st.experimental_rerun()
    
    
if __name__ == '__main__':
    main_ui()


