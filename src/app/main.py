from fastapi import FastAPI
import argparse
import configparser
import itertools
import requests
import sys
import signal
import threading
import time

app = FastAPI()


@app.get("/")
def read_root():
    session = requests.session()
    session.proxies = {
        'http':  'socks5h://tor:9050', 
        'https': 'socks5h://tor:9050'
    }

    robosatsTor = 'http://robosats6tkf3eva7x2voqso3a5wcorsnw34jveyxfqi2fu7oyheasid.onion'

    command = f'/api/book/?currency=1&type=0'

    api = f"https://hodlhodl.com/api/v1/offers?filters[side]=buy&filters[include_global]=true&filters[currency_code]=EUR&filters[only_working_now]=true&sort[by]=price"


    try:
        f = session.get(robosatsTor + command)
        #f = session.get(api)
    except IOError:
        print("Please, make sure you are running TOR!")
        exit(1)

    values = f.json()
    f.close()
    return {"nokyc": values}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/healthycheck")
def app_status():
    return {"healthy": "ok"}