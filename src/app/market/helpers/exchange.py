from proxy.tor import Tor

EXCHANGE_URL = 'http://wizpriceje6q5tdrxkyiazsgu7irquiqjy2dptezqhrtu7l2qelqktid.onion/getAllMarketPrices'

class Exchange:
  # Get the actual market price of btc depending of the requested currency.
  def get_fiat_price(fiat: str):
    try:
      fiat_prices = Tor.proxy_request(EXCHANGE_URL, 'EXCHANGE')
      # Check if we get exchange price object properly
      if ('data' in fiat_prices):
        for currency in fiat_prices['data']:
          if (currency['currencyCode'].lower() == fiat):
            return int(float(currency['price']))
      else:
        print(fiat_prices)
        print("Something went wrong while fetching exchange value")
        return None
    except IOError:
      print("Error: Could not get the exchange price!")
      return None