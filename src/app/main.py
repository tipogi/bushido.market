from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

from market.helpers.filters import BUY
from market.helpers.exchange import Exchange
from market.helpers.payment import Payment

# P2P markets
from market.bisq import Bisq
from market.hodlhodl import HodlHodl
from market.robosats import RoboSats
from market.lnp2pbot import Lnp2pBot

# Domain class
from proxy.domain import Domain

# Start the application
app = FastAPI()

# Define parameters default values
class MarketOptions(BaseModel):
    direction: Optional[str] = BUY
    fiat: Optional[str] = 'eur'
    premium: Optional[float] = 8

class PingOptions(BaseModel):
    domain: Optional[str]


'''
Get the market offers from a POST request
MARKETS: Bisq, HodlHodl, Robosats and LNP2PBot
All request goes through TOR network
'''
@app.post("/market_offers")
def market_offers(params: MarketOptions):
    # The offers currency
    fiat = params.fiat
    # The user action. If the user wants to buy we have to show sell offers
    # and viceversa. We will query to API to get offers types, not the user action
    direction = params.direction
    premium = params.premium

    exch_price = Exchange.get_fiat_price(fiat)
    # If we get the right price value, get the offers
    if exch_price is not None:
        bisq_offers = Bisq.market_offers(fiat, direction, premium, exch_price)
        hodlhodl_offers = HodlHodl.market_offers(fiat, direction, premium, exch_price)
        robosats_offers = RoboSats.market_offers(fiat, direction, premium)
        lnp2p_offers = Lnp2pBot.market_offers(fiat, direction, premium, exch_price)
        # Join all the offers
        allOffers = bisq_offers + hodlhodl_offers + robosats_offers + lnp2p_offers
        #allOffers = lnp2p_offers
        # and order by price depending the direction
        if (direction == BUY):
            allOffers.sort(key=lambda item: item.get('price'))
        else:
            allOffers.sort(key=lambda item: item.get('price'), reverse=True)

        return { "offers": allOffers, "price": exch_price }
    else:
        return { "offers": [], "price": 0}

'''
Check the domain status. All the ping requests goes through TOR service
'''
@app.post("/ping-domain")
def ping_domain(param: PingOptions):
    return Domain.check_domain_status(param.domain)

# Ping for temporal healthchecks from docker to see if the container is up
@app.get("/healthcheck")
def healthcheck():
    return 'healthy'

# Ping for temporal healthchecks from docker to see if the container is up
@app.get("/tor-healthcheck")
def healthcheck():
    return Domain.check_tor_status()