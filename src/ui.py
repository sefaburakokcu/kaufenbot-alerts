import os
import time
import copy
import json
import streamlit as st
import pandas as pd

import rerun

from threading import Thread

from backend import check_alert_status
from alarms import ExchangeClass, get_exchanges



def change_background(df):
    
    def highlight(row):
        '''
        highlight the maximum in a Series yellow.
        '''
        alerts = row['Alert']
        when = row["When"]
        if alerts == 1: 
            if when == 'above':
                css = 'background-color: green'
            else:
                css = 'background-color: red'
        else:
            css = 'background-color: white'
        return [css] * len(row)

    return df.style.apply(highlight, axis=1)


def choose_pair(exchange):
    symbols = exchange.get_symbols()
    pair = st.sidebar.selectbox("Choose a Pair", symbols)
    return pair 

def get_alert_params(pair):    
    with st.sidebar.form(key ='Form1'):
        alert_price =  st.number_input("Enter alert price:")
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

def delete_alerts(alerts, save_file='../cfg/alerts.json'):
    alerts_output = {}
    with st.sidebar.form(key ='Form2'):
        alert_index =  st.selectbox("Choose alert index which will be removed:", list(range(sum([len(x) for x in alerts.values()]))))
        delete_all = st.checkbox('Delete All')
        delete_alert_button = st.form_submit_button(label = 'Delete Selected Alerts')
    
    if delete_alert_button:
        if not delete_all:
            index = 0
            
            for pair, alerts_info in alerts.items():
                for alert_info in alerts_info:
                    
                    if index != alert_index:
                        if pair in alerts_output.keys():
                            alerts_output[pair].append(alert_info)
                        else:
                            alerts_output[pair] = [alert_info]
                    index += 1    
                    print(alerts_output)                               
    else:
        alerts_output = copy.deepcopy(alerts)
    with open(save_file, 'w') as outfile:
        json.dump(alerts_output, outfile)

                                               
    return alerts_output

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

        with open(f'{save_dir}alerts.json', 'w') as outfile:
            json.dump(alerts, outfile)

    alerts = delete_alerts(alerts, save_file='../cfg/alerts.json')
    
    df = get_df(alerts)
    
    df = change_background(df)
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


