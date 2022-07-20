from proxy.tor import Tor

BISQ_CLEAR = "https://bisq.markets"
BISQ_ONION = "http://bisqmktse2cabavbr2xjq7xw3h6g5ottemo5rolfcwt6aly6tp5fdryd.onion"
BISQ_FILTER = "/api/offers?market=btc_{}&direction={}"

class Bisq:
  def market_offers(fiat, direction, exch_price):
    filter = BISQ_FILTER.format(fiat.upper(), direction.upper())
    bisq_url = BISQ_ONION + filter
    response = Tor.proxy_request(bisq_url, 'BISQ')

    # If it fails to query bisq through onion address try from clearnet address
    if ("error" in response):
      bisq_url = BISQ_CLEAR + filter
      response = Tor.proxy_request(bisq_url, 'BISQ')

    # We will populate all offers filtering the fields that we want
    all_offers = []
    # To extract the results, we need to delete some keys from the response
    pair = f"btc_{fiat}"
    offer_type = direction + 's'

    if (pair in response) and (offer_type in response[pair]):
      for line in response[pair][offer_type]:
          offer = {}
          offer['exchange'] = 'Bisq'
          offer['price'] = int(float(line['price']))
          offer['dif'] = (offer['price'] / exch_price-1) * 100
          offer['min_btc'] = float(line['min_amount'])
          offer['max_btc'] = float(line['amount'])
          offer['min_amount'] = int(offer['min_btc'] * offer['price'])
          offer['max_amount'] = int(float(line['volume']))
          offer['method'] = line['payment_method']
          all_offers.append(offer)

      all_offers.sort(key=lambda item: item.get('price'))
      return all_offers
    else:
      return []