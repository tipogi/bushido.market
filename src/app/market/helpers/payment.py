# Exceptional Keywords
PAYPAL_FRIEND_AND_FAMILY = 'Paypal Friends & Family'
LN_NETWORK = 'Bitcoin Lightning Network'
LN_ICON = 'LN'
AMAZON = 'Amazon'
# When we find the above keyword, we will return that icon to the client
AMAZON_GIFT_CARD = 'AmazonGiftCard'
BINANCE_COIN = 'Binance Coin (BNB)'
BNB_ICON = 'BNB'
IN_PERSON = 'In person'
# Return payment type as it is
MONERO = 'Monero'
CASH_APP = 'CashApp'
HALCASH = 'HalCash'
N26 = 'N26'
REBELLION = 'Rebellion'
LITECOIN = 'Litecoin'
ZELLE = 'Zelle'
SKRILL = 'Skrill'
F2F = 'F2F'
CASH_BY_EMAIL = 'CASH_BY_EMAIL'
PAYPAL = 'Paypal'
AMAZON_GIFT_CARD_IN_ONE = 'AMAZON_GIFT_CARD'
# What is that? https://www.clearxchange.com/ -> Zelle icon
CLEAR_X_CHANGE = 'CLEAR_X_CHANGE'
# Return payment type after some processing
STRIKE = 'STRIKE'
STRIKE_LOWERCASE = 'Strike'
TRANSFERWISE = 'TRANSFERWISE'
TRANSFERWISE_LOWER = 'TransferWise'
WISE = 'Wise'
SEPA = 'SEPA'
SEPA_INSTANT = 'SEPA_INSTANT'
REVOLUT = 'REVOLUT'
REVOLUT_LOWERCASE = 'Revolut'
BIZUM = 'BIZUM'
BIZUM_LOWERCASE = 'Bizum'
TETHER = 'Tether'
USDT = 'USDT'
# Keywords that we will ignore
IGNORE = 'Ignore'
INSTANT = 'Instant'

PAYMENT_STATIC = [
  {
    "order": "bisq",
    "method": "Revolut Instant SEPA Wise AMAZON_GIFT_CARD",
    "amount": 250
  },
  {
    "order": "robo",
    "method": "Revolut Paypal Wise Instant SEPA",
    "amount": 122
  },
  {
    "order": "robo",
    "method": "Paypal Friends & Family",
    "amount": 122
  },
  {
    "order": "hodlhodl",
    "method": "Amazon Gift Card",
    "amount": 122
  },
  {
    "order": "hodlhodl",
    "method": "Binance Coin (BNB)",
    "amount": 122
  }
]

class Payment:

  def model_orders_payments_types():
    for order in PAYMENT_STATIC:
      paymentMethodsArray = Payment.__loopOrderPaymentsMethods(order["method"])
      print (paymentMethodsArray)
    return PAYMENT_STATIC

  def loopOrderPaymentsMethods(paymentMethods):
    # Convert payment methods string in an array to after loop
    icon, others, paymentMethodArray = [], [], paymentMethods.split()
    exceptionIcon = Payment.__checkExceptionalPaymentIcons(paymentMethods)
    if (exceptionIcon is None):
      # Loop payment method array
      for paymentType in paymentMethodArray:
        newKeyword = Payment.__createNewMethodKeyword(paymentType)
        # The method does not have icon so, I threat as a other payment method
        if (newKeyword is None):
          others.append(paymentType)
        elif (newKeyword == IGNORE):
          print('Ignore')
        else:
          icon.append(newKeyword)
    else:
      icon.append(exceptionIcon)
    return { "icon": icon, "others": others }

  def __createNewMethodKeyword(paymentType):
    if (
        paymentType == MONERO or 
        paymentType == CASH_APP or 
        paymentType == HALCASH or 
        paymentType == REBELLION or 
        paymentType == N26 or 
        paymentType == LITECOIN or
        paymentType == ZELLE or 
        paymentType == SKRILL or 
        paymentType == F2F or 
        paymentType == CASH_BY_EMAIL or 
        paymentType == PAYPAL or
        paymentType == AMAZON_GIFT_CARD_IN_ONE or 
        paymentType == CLEAR_X_CHANGE
    ):
      return paymentType
    elif paymentType == STRIKE or paymentType == STRIKE_LOWERCASE:
      return STRIKE_LOWERCASE
    elif paymentType == TRANSFERWISE or paymentType == TRANSFERWISE_LOWER or paymentType == WISE:
      return WISE
    elif paymentType == SEPA or paymentType == SEPA_INSTANT:
      return SEPA
    elif paymentType == REVOLUT or paymentType == REVOLUT_LOWERCASE:
      return REVOLUT_LOWERCASE
    elif paymentType == BIZUM or paymentType == BIZUM_LOWERCASE:
      return BIZUM
    elif paymentType == TETHER or paymentType == USDT:
      return TETHER
    elif paymentType == INSTANT:
      return IGNORE
    else:
      return None
    
  # Check always at the beginning if we have that string chain. If we have return that icon
  def __checkExceptionalPaymentIcons(paymentMethods):
    if (paymentMethods.split()[0] == AMAZON):
      return AMAZON_GIFT_CARD
    elif paymentMethods == PAYPAL_FRIEND_AND_FAMILY:
      return PAYPAL
    elif paymentMethods == LN_NETWORK:
      return LN_ICON
    elif paymentMethods == BINANCE_COIN:
      return BNB_ICON
    elif paymentMethods == IN_PERSON:
      return F2F
    else:
      return None
