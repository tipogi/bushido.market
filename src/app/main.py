from fastapi import FastAPI
import argparse
import configparser
import itertools
import requests
import sys
import signal
import threading
import time
import json

from market.bisq import BISQ_URL 
from market.robosats import ROBOSATS_URL 
from market.hodlhodl import HODLHODL_URL

app = FastAPI()



@app.get("/")
def read_root():
    return {"root": "me"}

    


@app.get("/robosats")
def robosats_market():
    session = requests.session()
    session.proxies = {
        'http':  'socks5h://tor:9050', 
        'https': 'socks5h://tor:9050'
    }
    try:
        f = session.get(ROBOSATS_URL)
    except IOError:
        print("Please, make sure you are running TOR!")
        exit(1)

    values = f.json()
    f.close()
    return {"nokyc": values}

@app.get("/bisq")
def bisq_market():
    session = requests.session()
    session.proxies = {
        'http':  'socks5h://tor:9050', 
        'https': 'socks5h://tor:9050'
    }
    try:
        f = session.get(BISQ_URL)
        values = f.json()
        f.close()
        return {"nokyc": values}
    except json.JSONDecodeError:
        print("We could not get any response back. It seams the service is down")
        return { 'error': 'BISQ service down'}
    except IOError:
        print("Please, make sure you are running TOR!")
        exit(1)
    

    

@app.get("/hodlhodl")
def hodlhodl_market():
    session = requests.session()
    session.proxies = {
        'http':  'socks5h://tor:9050', 
        'https': 'socks5h://tor:9050'
    }
    try:
        f = session.get(HODLHODL_URL)
    except IOError:
        print("Please, make sure you are running TOR!")
        exit(1)

    values = f.json()
    f.close()
    return {"nokyc": values}

@app.get("/market")
def market():
    return {
        "robosats": ROBOSATS_URL,
        "bisq": BISQ_URL,
        "hodlhodl": HODLHODL_URL
    }