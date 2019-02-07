# coding: utf8

import requests, random

def guess():
    
    usage = 'Usage: !guess'
    file = open("/home/matt/Games/twitch-bot-master/src/res/guess.txt","r")
    locations = []
    for line in file: 
        locations.append(line.strip())
    size = len(locations)
    randomIndex=random.randint(0, size-1)
    try:
        file.close()
        
        return 'I guess '+locations[randomIndex]
    except Exception as e:
        file.close()
        return usage
        
