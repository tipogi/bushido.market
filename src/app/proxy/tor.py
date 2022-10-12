import requests
import json

MARKET_TIMEOUT = 20.0
DOMAIN_TIMEOUT = 30.0
HTTP_SOCKET_URL = 'socks5h://tor:9050'
HTTPS_SOCKET_URL = 'socks5h://tor:9050'

# If I add in domain.py, it will have circular dependency
DOMAIN_REQUEST = 'DOMAIN_CHECK'

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
      if (request_name == DOMAIN_REQUEST):
        return type(err).__name__
      else:
        print("Please, make sure you are running TOR!")  
        #exit(1)
        return []