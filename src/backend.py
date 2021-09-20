import os
import time
import json
import copy

from alarms import ExchangeClass

DELAY = 60

def check_alert_status(file_name="../cfg/alerts.json"):
    while not os.path.exists(file_name):
        time.sleep(DELAY)

    
    exchange = ExchangeClass('binance')
    initial_time = os.stat(file_name).st_mtime
    
    with open(file_name) as json_file:
        alerts = json.load(json_file)
            
    previous_alerts = copy.deepcopy(alerts)
    
    while True:
        time.sleep(DELAY)
        alerts = exchange.get_alerts(alerts)
        if (alerts != previous_alerts):
            with open(file_name,'w') as outfile:
                json.dump(alerts, outfile)
                
            previous_alerts = copy.deepcopy(alerts)
    
        last_modified_time = os.stat(file_name).st_mtime
        
        if (last_modified_time != initial_time):
            with open(file_name) as json_file:
                alerts = json.load(json_file)
            previous_alerts = copy.deepcopy(alerts)
            initial_time = last_modified_time
            with open("rerun.py", "w") as f:
                f.write(f'timestamp = "{time.time()}"')


if __name__ == '__main__':            
                
    check_alert_status(file_name="../cfg/alerts.json")