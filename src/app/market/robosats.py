from proxy.tor import Tor
from market.helpers.filters import SELL, BUY, Filter, ONLINE, RECENTLY_ONLINE, OFFLINE
from market.helpers.payment import Payment

# Check in the robosats github the url
ROBOSATS_ONION = "http://robosats6tkf3eva7x2voqso3a5wcorsnw34jveyxfqi2fu7oyheasid.onion"
ROBOSATS_FILTER = "/api/book/?currency={}&type={}"

# Offer actual state
ACTIVE = "Active"
SEEN_RECENTLY = "Seen Recently"
INACTIVE = "Inactive"

currencies = {
  "1":"USD", 
  "2":"EUR", 
  "3":"JPY", 
  "4":"GBP", 
  "5":"AUD", 
  "6":"CAD", 
  "7":"CHF",
  "8":"CNY", 
  "9":"HKD", 
  "10":"NZD", 
  "11":"SEK", 
  "12":"KRW", 
  "13":"SGD",
  "14":"NOK",
	"15":"MXN", 
  "16":"KRW", 
  "17":"RUB", 
  "18":"ZAR", 
  "19":"TRY",
  "20":"BRL", 
  "21":"CLP", 
  "22":"CZK", 
  "23":"DKK", 
  "24":"HRK", 
  "25":"HUF", 
  "26":"INR", 
  "27":"ISK", 
  "28":"PLN",
	"29":"RON", 
  "30":"ARS", 
  "31":"VES", 
  "32":"COP", 
  "33":"PEN", 
  "34":"UYU", 
  "35":"PYG", 
  "36":"BOB", 
  "37":"IDR", 
  "38":"ANG", 
  "39":"CRC", 
  "40":"CUP", 
  "41":"DOP", 
  "42":"GHS",
	"43":"GTQ", 
  "44":"ILS", 
  "45":"JMD",
  "46":"KES", 
  "47":"KZT", 
  "48":"MYR", 
  "49":"NAD",
  "50":"NGN", 
  "51":"AZN", 
  "52":"PAB", 
  "53":"PHP", 
  "54":"PKR", 
  "55":"QAR", 
  "56":"SAR", 
  "57":"THB", 
  "58":"TTD", 
  "59":"VND", 
  "60":"XOF", 
  "61":"TWD", 
  "300":"XAU", 
  "1000":"BTC"
}

class RoboSats:
  # Get the API request query
  def getQuery(fiat: str, direction: str):
    key_list = list(currencies.keys())
    val_list = list(currencies.values())
    index = val_list.index(fiat.upper())
    # In that case, currency is a integer not a currency symbol
    currency = key_list[index]
    
    # Get the buy offers
    if (direction == SELL):
      # In robosats the buy type offers are defined with the 0 number
      typeoffer = 0
    # Get the sell offers
    elif (direction == BUY):
      # The sell offers are defined with the 1 number
      typeoffer = 1
    else:
      # Get all the offers
      typeoffer = 2

    return ROBOSATS_FILTER.format(currency, typeoffer)

  # Get the same status as HodlHodl
  def get_maker_status(status: str):
    if (status == ACTIVE):
      return ONLINE
    elif (status == SEEN_RECENTLY):
      return RECENTLY_ONLINE
    else:
      return OFFLINE

  def market_offers(fiat: str, direction: str, premium: float):
    # Create request filter
    filter = RoboSats.getQuery(fiat, direction)
    # Create the API request URL
    robosats_url = ROBOSATS_ONION + filter
    # Make request to get offers
    robosats_offers = Tor.proxy_request(robosats_url, 'ROBOSATS')

    # We will populate all offers filtering the fields that we want
    all_offers = []
    
    for robosats_offer in robosats_offers:
      # Get some fields before add an offer
      offer_premium = float(robosats_offer['premium'])
      offer_type = Filter.get_offer_types(direction)

      if (Filter.offer_premium_accepted(offer_type, offer_premium, premium)):
        offer = {}
        offer['exchange'] = 'Robosats'

        offer['price'] = int(float(robosats_offer['price']))
        offer['dif'] = "%{:.2f}".format(offer_premium)

        # Get the offer online status
        offer['maker_status'] = RoboSats.get_maker_status(robosats_offer['maker_status'])

        if (robosats_offer['amount'] is not None):
          offer['min_amount'] = int(float(robosats_offer['amount']))
          offer['max_amount'] = int(float(robosats_offer['amount']))
        else:
          offer['min_amount'] = int(float(robosats_offer['min_amount']))
          offer['max_amount'] = int(float(robosats_offer['max_amount']))

        offer['min_btc'] = offer['min_amount'] / offer['price']
        offer['max_btc'] = offer['max_amount'] / offer['price']
        offer['method'] = Payment.loopOrderPaymentsMethods(robosats_offer['payment_method'])

        # Add the offer in the offers array  
        all_offers.append(offer)

    return all_offers

  