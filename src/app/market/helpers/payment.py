# Exceptional Keywords
PAYPAL_FRIEND_AND_FAMILY = 'Paypal Friends & Family'
LN_NETWORK = 'Bitcoin Lightning Network'
LN_ICON = 'LN'
AMAZON = 'Amazon'
GOOGLE_PLAY = 'Google play Gift card'
APPLE_PAY = 'Apple Pay'
# When we find the above keyword, we will return that icon to the client
AMAZON_GIFT_CARD = 'AmazonGiftCard'
BINANCE_COIN = 'Binance Coin (BNB)'
BNB_ICON = 'BNB'
IN_PERSON = 'In person'
# Return payment type as it is
MONERO = 'Monero'
CASH_APP = 'CashApp'
CASH_APP_SEP = 'Cash App'
N26 = 'N26'
REBELLION = 'Rebellion'
LITECOIN = 'Litecoin'
ZELLE = 'Zelle'
SKRILL = 'Skrill'
F2F = 'F2F'
CASH_BY_MAIL = 'CASH_BY_MAIL'
PAYPAL = 'Paypal'
PAYPAL_UP = 'PayPal'
AMAZON_GIFT_CARD_IN_ONE = 'AMAZON_GIFT_CARD'
VENMO = 'Venmo'
LIQUID = 'Liquid'
LONG_E_TRANS = 'INTERAC_E_TRANSFER'
BROKEN_E_TRANS = 'Interac e-transfer'
E_TRANSFER = 'e-trans'
# What is that? https://www.clearxchange.com/ -> Zelle icon
CLEAR_X_CHANGE = 'CLEAR_X_CHANGE'
# Return payment type after some processing
STRIKE = 'STRIKE'
UPHOLD = 'UPHOLD'
STRIKE_LOWERCASE = 'Strike'
TRANSFERWISE = 'TRANSFERWISE'
TRANSFERWISE_LOWER = 'TransferWise'
WISE = 'Wise'
SEPA = 'SEPA'
SEPA_INSTANT = 'SEPA_INSTANT'
ANY_NATIONAL_BANK = "Any national bank"
REVOLUT = 'REVOLUT'
REVOLUT_LOWERCASE = 'Revolut'
BIZUM = 'BIZUM'
BIZUM_LOWERCASE = 'Bizum'
AU_PAYID = 'AUSTRALIA_PAYID'
AU_PAYID_SHORT = 'PayID'
TETHER = 'Tether'
USDT = 'USDT'
HALCASH = 'HalCash'
HALCASH_SLASH = 'Hal-cash'
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
          print('The offer does not have icon so, ignore')
        else:
          icon.append(newKeyword)
    else:
      icon.append(exceptionIcon)
    return { "icons": icon, "others": others }

  def __createNewMethodKeyword(paymentType):
    if (
        paymentType == MONERO or 
        paymentType == CASH_APP or
        paymentType == REBELLION or 
        paymentType == N26 or 
        paymentType == LITECOIN or
        paymentType == ZELLE or 
        paymentType == SKRILL or 
        paymentType == F2F or 
        paymentType == CASH_BY_MAIL or 
        paymentType == CLEAR_X_CHANGE or 
        paymentType == VENMO or 
        paymentType == LIQUID or 
        paymentType == AU_PAYID or
        paymentType == UPHOLD
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
      return BIZUM_LOWERCASE
    elif paymentType == PAYPAL or paymentType == PAYPAL_UP:
      return PAYPAL
    elif paymentType == HALCASH or paymentType == HALCASH_SLASH:
      return HALCASH
    elif paymentType == TETHER or paymentType == USDT:
      return TETHER
    elif paymentType == AMAZON_GIFT_CARD_IN_ONE:
      return AMAZON_GIFT_CARD
    elif paymentType == LONG_E_TRANS:
      return E_TRANSFER
    elif paymentType == AU_PAYID_SHORT:
      return AU_PAYID
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
    #elif paymentMethods == BINANCE_COIN:
      #return BNB_ICON
    elif paymentMethods == IN_PERSON:
      return F2F
    elif paymentMethods == ANY_NATIONAL_BANK:
      return ANY_NATIONAL_BANK
    elif paymentMethods == GOOGLE_PLAY:
      return GOOGLE_PLAY
    elif paymentMethods == APPLE_PAY:
      return APPLE_PAY
    elif paymentMethods == BROKEN_E_TRANS:
      return E_TRANSFER
    elif paymentMethods == CASH_APP_SEP:
      return CASH_APP
    else:
      return None
