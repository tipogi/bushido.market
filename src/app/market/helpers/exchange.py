from proxy.tor import Tor

EXCHANGE_URL = 'http://wizpriceje6q5tdrxkyiazsgu7irquiqjy2dptezqhrtu7l2qelqktid.onion/getAllMarketPrices'
YADIO_API = 'https://api.yadio.io/exrates/{}'

class Exchange:
  # Get the actual market price of btc depending of the requested currency.
  def get_fiat_price(fiat: str):
    try:
      tor_wiz_rates = Tor.proxy_request(EXCHANGE_URL, 'EXCHANGE_WIZ')
      # Check if we get exchange price object properly
      if ('data' in tor_wiz_rates):
        for currency in tor_wiz_rates['data']:
          if (currency['currencyCode'].lower() == fiat):
            print('Exchange rate downloaded from Wiz Tor instance')
            return int(float(currency['price']))
      else:
        print(tor_wiz_rates)
        print("Something went wrong while fetching the exchange rate fron Wiz, trying yadio.io...")
        return Exchange.get_yadio(fiat)
    except IOError:
      print("Error: Could not get the exchange price!")
      return None
  def get_yadio(fiat: str):
    url = YADIO_API.format(fiat.upper())
    yadio_rates = Tor.proxy_request(url, 'YADIO')
    if ("BTC" in yadio_rates):
      print('Exchange rate downloaded from Yadio API')
      return int(yadio_rates['BTC'])
    else:
      return None