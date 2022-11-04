import requests
import json

MARKET_TIMEOUT = 10.0
EXTRA_TIMEOUT = 20.0
DOMAIN_TIMEOUT = 30.0
HTTP_SOCKET_URL = 'socks5h://tor-proxy:9050'
HTTPS_SOCKET_URL = 'socks5h://tor-proxy:9050'

# If I add in domain.py, it will have circular dependency
DOMAIN_REQUEST = 'DOMAIN_CHECK'
DOMAIN_UNREACHEABLE_ERROR = 'Failed to establish a new connection: 0x04: Host unreachable'
HOST_UNREACHEABLE_MESSAGE = 'Host unreacheable'
TOR_SERVICE_DOWN = 'Name or service not known'

class Tor:
  # Make a request throw the Tor Proxy
  def proxy_request(url: str, request_name: str):
    try:
      session = requests.session()
      # Add the Tor proxy server urls
      session.proxies = {
          'http':  HTTP_SOCKET_URL, 
          'https': HTTPS_SOCKET_URL
      }
      # Set the timeout request limit
      timeout_limit = MARKET_TIMEOUT if request_name != DOMAIN_REQUEST else DOMAIN_TIMEOUT
      # By average the bisq and Robosats requests take more time that other markets
      if request_name == 'BISQ' or request_name == 'ROBOSATS':
        timeout_limit = EXTRA_TIMEOUT
      # Make request
      request = session.get(url, timeout=timeout_limit)
      response = request
      # Parse to JSON the response to after loop each element
      if (request_name != DOMAIN_REQUEST):
        response = request.json()
      # Finish request
      request.close()
      return response
    except json.JSONDecodeError:
      print(request_name + ": We could not get any response back. It seams the service is down")
      return []
    except requests.Timeout:
      print(f"The request of {request_name} take too long, try again")
      return []
    except IOError as err:
      # Use that to not mix with market requests
      if (request_name == DOMAIN_REQUEST):
        errorCastToString = str(err)
        print(errorCastToString)
        # We found that message in the error
        if (errorCastToString.find(DOMAIN_UNREACHEABLE_ERROR) != -1):
          print("We could not access to the DOMAIN. It seems it is DOWN")
          return HOST_UNREACHEABLE_MESSAGE
        else:
          print("TOR service is DOWN. We could not proxy the request through TOR network")
          return type(err).__name__
      else:
        print("Please, make sure you are running TOR!")  
        #exit(1)
        return []