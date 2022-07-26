from operator import truediv
from market.helpers.Filters import Filter, BUY
from proxy.Tor import Tor

HOLDHODL_API = "https://hodlhodl.com/api/v1/offers?"
HOLDHODL_FILTER = "filters[side]={}&filters[include_global]=true&filters[currency_code]={}&filters[only_working_now]=true&sort[by]=price"

# Payment Methods
SEPA = "SEPA"
ANY_NATIONAL_BANK = "Any national bank"
NATIONAL_BANK = "National Bank"

class HodlHodl:

  def market_offers(fiat: str, direction: str, premium: float, exch_price: float) -> list:
    # Create request filter
    offer_type = Filter.get_offer_types(direction)
    filter = HOLDHODL_FILTER.format(offer_type.upper(), fiat.upper())
    # Create the API request URL
    hodlhodl_url = HOLDHODL_API + filter
    # Make request to get offers
    hodlhodl_offers = Tor.proxy_request(hodlhodl_url, 'HODLHODL')
    
    # We will populate all offers filtering the fields that we want
    all_offers = []
    
    for hodlhodl_offer in hodlhodl_offers['offers']:
      # Check offer status
      status = hodlhodl_offer['trader']['online_status']
      offers_price = int(float(hodlhodl_offer['price']))
      offer_premium = (offers_price / exch_price - 1) * 100
      
      if (Filter.offer_premium_accepted(offer_type, offer_premium, premium)):
        # Create new object to add the new properties
        offers = {}
        offers['exchange'] = "HodlHodl"

        offers['price'] = offers_price
        offers['dif'] = offer_premium
        offers['currency'] = hodlhodl_offer['currency_code']

        # Get the offer online status
        offers['maker_status'] = status

        offers['min_amount'] = int(float(hodlhodl_offer['min_amount']))
        offers['max_amount'] = int(float(hodlhodl_offer['max_amount']))

        # Calculate min and max in btc
        offers['min_btc'] = offers['min_amount'] / offers['price']
        offers['max_btc'] = offers['max_amount'] / offers['price']
        
        if ( offer_type == BUY ):
          offers['method'] = hodlhodl_offer['payment_methods'][0]['name']
        else:
          offers['method'] = hodlhodl_offer['payment_method_instructions'][0]['payment_method_name']

        if SEPA in offers['method']:
          offers['method'] = SEPA
        elif ANY_NATIONAL_BANK in offers['method']:
          offers['method'] = NATIONAL_BANK

        # Add the offer in the offers array  
        all_offers.append(offers)

    return all_offers