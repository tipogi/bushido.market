from proxy.tor import Tor

EXCHANGE_URL = 'http://wizpriceje6q5tdrxkyiazsgu7irquiqjy2dptezqhrtu7l2qelqktid.onion/getAllMarketPrices'

class Exchange:
  def get_fiat_price(fiat):
    fiat_prices = Tor.proxy_request(EXCHANGE_URL, 'EXCHANGE')
    for currency in fiat_prices['data']:
            if (currency['currencyCode'].lower() == fiat):
                return int(float(currency['price']))