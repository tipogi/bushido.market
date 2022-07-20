import requests
import json

class Tor:
  def proxy_request(url, market_name):
    try:
      session = requests.session()
      session.proxies = {
          'http':  'socks5h://tor:9050', 
          'https': 'socks5h://tor:9050'
      }
      request = session.get(url)
      response = request.json()
      request.close()
      return response
    except json.JSONDecodeError:
        print(market_name + ": We could not get any response back. It seams the service is down")
        return { 'error': 'Requested service down'}
    except IOError:
        print("Please, make sure you are running TOR!")
        exit(1)