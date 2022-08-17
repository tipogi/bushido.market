from market.helpers.filters import Filter, ONLINE
from proxy.tor import Tor
from market.helpers.payment import Payment

BISQ_CLEAR = "https://bisq.markets"
BISQ_ONION = "http://bisqmktse2cabavbr2xjq7xw3h6g5ottemo5rolfcwt6aly6tp5fdryd.onion"
BISQ_FILTER = "/api/offers?market=btc_{}&direction={}"

class Bisq:

  def market_offers(fiat: str, direction: str, premium: float, exch_price: float):
    # Create request filter
    offer_type = Filter.get_offer_types(direction)
    filter = BISQ_FILTER.format(fiat.upper(), offer_type.upper())
    # Create the API request URL
    bisq_url = BISQ_ONION + filter
    # Make request to get offers
    bisq_offers = Tor.proxy_request(bisq_url, 'BISQ')

    # If it fails to query bisq through onion address try from clearnet address
    if ("error" in bisq_offers):
      bisq_url = BISQ_CLEAR + filter
      bisq_offers = Tor.proxy_request(bisq_url, 'BISQ')

    # We will populate all offers filtering the fields that we want
    all_offers = []

    # To extract the bisq offers, we need to ignore some keys from the response
    pair = f"btc_{fiat}"
    offer_type_key = offer_type + 's'

    # Before get the offers, check if the keys exist in the offers array
    if (pair in bisq_offers) and (offer_type_key in bisq_offers[pair]):
      for bisq_offer in bisq_offers[pair][offer_type_key]:
        offers_price = int(float(bisq_offer['price']))
        offer_premium = (offers_price / exch_price - 1) * 100
        # Check if that offer satisfy user request: Premium
        if (Filter.offer_premium_accepted(offer_type, offer_premium, premium)):
          offer = {}
          offer['exchange'] = 'Bisq'
          offer['price'] = offers_price
          offer['dif'] = "%{:.2f}".format(offer_premium)
          offer['maker_status'] = ONLINE
          offer['min_btc'] = float(bisq_offer['min_amount'])
          offer['max_btc'] = float(bisq_offer['amount'])
          offer['min_amount'] = int(offer['min_btc'] * offer['price'])
          offer['max_amount'] = int(float(bisq_offer['volume']))
          offer['method'] = Payment.loopOrderPaymentsMethods(bisq_offer['payment_method'])

          # Add the offer in the offers array  
          all_offers.append(offer)
      return all_offers
    else:
      return []