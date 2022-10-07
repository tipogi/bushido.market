from proxy.tor import Tor

from market.helpers.payment import Payment
from market.helpers.filters import ONLINE

LNP2PBOT_API='https://api.lnp2pbot.com/orders'

class Lnp2pBot:
    def market_offers(currency: str, direction: str, premium: float, exch_price: float):
        lnp2p_request = Tor.proxy_request(LNP2PBOT_API, 'LNP2PBOT')
        fiat = currency.upper()
        offer_type = direction.lower()
        print('fiat:', fiat, 'direction:', offer_type)
        all_offers = []
        if (len(lnp2p_request) > 0):
            for offer in lnp2p_request:
                if (offer['type'] == offer_type and offer['fiat_code'] == fiat):
                    p2p_offer = {}
                    offer_limits = Lnp2pBot.min_max_amount(offer)
                    p2p_offer['exchange'] = 'LnP2PBot'
                    p2p_offer['_id'] = offer['_id']
                    p2p_offer['min_amount'] = int(offer_limits['min'])
                    p2p_offer['max_amount'] = int(offer_limits['max'])
                    p2p_offer['method'] = Payment.loopOrderPaymentsMethods(offer['payment_method'])
                    premium = offer['price_margin']
                    p2p_offer['price'] = Lnp2pBot.calculatePrice(exch_price, premium)
                    # Get the offer online status
                    p2p_offer['maker_status'] = ONLINE
                    p2p_offer['dif'] = "%{:.2f}".format(premium)

                    #_id
                    #status
                    #price_margin

                    print(p2p_offer)
        else:
            return all_offers

    def min_max_amount(offer):
        fiat_amount = offer['fiat_amount']
        min_amount = offer['min_amount']
        max_amount = offer['max_amount']
        response = {}
        if (fiat_amount is None):
            response['min'] = min_amount
            response['max'] = max_amount
        else:
            response['min'] = fiat_amount
            response['max'] = fiat_amount
        return response

    def calculatePrice(market_price, premium):
        calc = (market_price / 100) * premium
        return market_price + calc

