import requests
import json

class Tor:
  # Make a request throw the Tor Proxy
  def proxy_request(url: str, market_name: str):
    try:
      session = requests.session()
      # Add the Tor proxy server urls
      session.proxies = {
          'http':  'socks5h://tor:9050', 
          'https': 'socks5h://tor:9050'
      }
      # Make request
      request = session.get(url, timeout=10.0)
      response = request.json()
      # Finish request
      request.close()
      return response
    except json.JSONDecodeError:
      print(market_name + ": We could not get any response back. It seams the service is down")
      return []
    except requests.Timeout as err:
      print(f"The request of {market_name} take too long, try again")
      return []
    except IOError:
      print("Please, make sure you are running TOR!")
      #exit(1)
      return []