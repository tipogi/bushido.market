from proxy.tor import Tor

ROBOSATS_ONION = "http://robosats6tkf3eva7x2voqso3a5wcorsnw34jveyxfqi2fu7oyheasid.onion"
ROBOSATS_FILTER = "/api/book/?currency={}&type={}"

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
  def getQuery(fiat, direction):
    key_list = list(currencies.keys())
    val_list = list(currencies.values())
    index = val_list.index(fiat.upper())
    # In that case, currency is a integer not a currency symbol
    currency = key_list[index]

    if (direction == "sell"):
        typeoffer = 1
    else:
        typeoffer = 0

    return ROBOSATS_FILTER.format(currency, typeoffer)

  def market_offers(fiat, direction):
    filter = RoboSats.getQuery(fiat, direction)
    robosats_url = ROBOSATS_ONION + filter

    response = Tor.proxy_request(robosats_url, 'ROBOSATS')

    all_offers = []

    for robo_offer in response:
      if (robo_offer == "not_found"):
        break
      offer = {}
      offer['exchange'] = 'Robosats'
      offer['price'] = int(float(robo_offer['price']))
      offer['dif'] = float(robo_offer['premium'])

      if (robo_offer['amount'] is not None):
        offer['min_amount'] = int(float(robo_offer['amount']))
        offer['max_amount'] = int(float(robo_offer['amount']))
      else:
        offer['min_amount'] = int(float(robo_offer['min_amount']))
        offer['max_amount'] = int(float(robo_offer['max_amount']))
        offer['min_btc'] = offer['min_amount']/offer['price']
        offer['max_btc'] = offer['max_amount']/offer['price']
        offer['method'] = robo_offer['payment_method']
        all_offers.append(offer)

      all_offers.sort(key=lambda item: item.get('price'))

      return all_offers

  