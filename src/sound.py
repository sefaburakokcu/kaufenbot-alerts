#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 17:35:55 2021

@author: sefa
"""

import json
import time
from playsound import playsound



def check_alerts_and_play_sound(file_name='../cfg/alerts.json'):
    with open(file_name) as json_file:
        alerts = json.load(json_file)
    
    alert = False
    
    for pair, alerts_info in alerts.items():
        for i, alert_info in enumerate(alerts_info):
            if (alert_info['alert_status']):
                alert = True 
                return alert
    return alert
                

def check_sound_status(sound_cfg='../cfg/sound.json'):
    with open(sound_cfg) as json_file:
        alert_info = json.load(json_file)
        
    alert_sound = alert_info["alert_sound"]
    return alert_sound

    
def play(alert_cfg, sound_cfg, sound_file='../inputs/sound/Crystal.mp3'):
    alert = check_alerts_and_play_sound(alert_cfg)
    sound =check_sound_status(sound_cfg)
    
    if alert and sound:
        playsound(sound_file)
        
def main():
    alert_cfg = '../cfg/alerts.json'
    sound_cfg = '../cfg/sound.json'
    sound_file='../inputs/sound/Crystal.mp3'
    while True:
        time.sleep(1)
        play(alert_cfg, sound_cfg, sound_file)
        
        
if __name__ == '__main__':
    main()
    