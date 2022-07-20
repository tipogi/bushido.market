from proxy.tor import Tor

HOLDHODL_API = "https://hodlhodl.com/api/v1/offers?"
HOLDHODL_FILTER = "filters[side]={}&filters[include_global]=true&filters[currency_code]={}&filters[only_working_now]=true&sort[by]=price"

class HodlHodl:
  def market_offers(fiat, direction, exch_price):
    filter = HOLDHODL_FILTER.format(direction.upper(), fiat.upper())
    hodlhodl_url = HOLDHODL_API + filter

    response = Tor.proxy_request(hodlhodl_url, 'HODLHODL')
    
    # We will populate all offers filtering the fields that we want
    all_offers = []
    
    for offer in response['offers']:
      offers = {}
      offers['exchange'] = "HodlHodl"
      offers['price'] = int(float(offer['price']))
      offers['dif'] = (offers['price'] / exch_price - 1) * 100
      offers['currency'] = offer['currency_code']
      offers['min_amount'] = int(float(offer['min_amount']))
      offers['max_amount'] = int(float(offer['max_amount']))
      offers['min_btc'] = offers['min_amount']/offers['price']
      offers['max_btc'] = offers['max_amount']/offers['price']
      status = offer['trader']['online_status']

      if (direction == "buy"):
        offers['method'] = offer['payment_methods'][0]['name']
      else:
        offers['method'] = offer['payment_method_instructions'][0]['payment_method_name']

      if "SEPA" in offers['method']:
        offers['method'] = "SEPA"
      elif "Any national bank" in offers['method']:
        offers['method'] = "NATIONAL_BANK"
      # Still to decide which offers filter
      # Status: offline, recently_online, online
      if (status == 'online'):
        all_offers.append(offers)
        
    all_offers.sort(key=lambda item: item.get("price"))

    return all_offers