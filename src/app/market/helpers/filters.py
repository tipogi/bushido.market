# User action
BUY = "buy"
SELL = "sell"

# Offer actual state
ONLINE = "online"
RECENTLY_ONLINE = "recently online"
OFFLINE = "offline"

class Filter:

  # The user action has to get the opposite offer types.
  # If user wants to buy, it has to get sell offers and viceversa
  
  # Get the offer types to show the user available options
  def get_offer_types(direction: str) -> str:
    return BUY if direction == SELL else SELL

  # Check the offer premium if it is inside of the range
  def offer_premium_accepted(offer: str, offer_premium: float, premium: float):
    # Not selling below that premium percentage
    if (offer == BUY and offer_premium > -premium):
      return True
    # Not buying above that premium percentage
    elif (offer == SELL and offer_premium < premium):
      return True
    else: 
      return False