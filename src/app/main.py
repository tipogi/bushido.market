from fastapi import FastAPI

from market.exchange import Exchange
from market.bisq import Bisq
from market.hodlhodl import HodlHodl
from market.robosats import RoboSats

app = FastAPI()


# Ping temporal healthchecks from docker to see if the container is up
@app.get("/healthcheck")
def healthcheck():
    return 'healthy'

@app.get("/market_offers")
def market_offers():
    fiat = "eur"
    direction = "buy"

    exch_price = Exchange.get_fiat_price(fiat)
    
    bisq_offers = Bisq.market_offers(fiat, direction, exch_price)
    hodlhodl_offers = HodlHodl.market_offers(fiat, direction, exch_price)
    robosats_offers = RoboSats.market_offers(fiat, direction)
    # Join all the offers
    allOffers = bisq_offers + hodlhodl_offers + robosats_offers
    # and order by price depending the direction
    if (direction =='sell'):
        allOffers.sort(key=lambda item: item.get('price'))
    else:
        allOffers.sort(key=lambda item: item.get('price'), reverse=True)

    return allOffers

@app.get("/urls")
def market():
    return {
        "robosats": "http://robosats6tkf3eva7x2voqso3a5wcorsnw34jveyxfqi2fu7oyheasid.onion/api/book/?currency=2&type=0",
        "bisq": "http://bisqmktse2cabavbr2xjq7xw3h6g5ottemo5rolfcwt6aly6tp5fdryd.onion/api/offers?market=btc_EUR&direction=BUY",
        "hodlhodl": "https://hodlhodl.com/api/v1/offers?filters[side]=buy&filters[include_global]=true&filters[currency_code]=EUR&filters[only_working_now]=true&sort[by]=price"
    }