from http.client import HTTPException
from requests import HTTPError
from proxy.tor import TOR_SERVICE_DOWN
from proxy.tor import Tor, DOMAIN_REQUEST

#Down url
#STATIC_URL = 'https://dyinodes.com/'
STATIC_URL = 'https://bitcoiner.guide/'

class Domain:
  def check_domain_status(domain):
    pingStatus = Tor.proxy_request(domain, DOMAIN_REQUEST)
    if (hasattr(pingStatus, 'status_code')):
      return pingStatus.status_code
    # Object is array
    elif (type(pingStatus).__name__ == 'str'):
        return pingStatus
    # If there is some error with tor proxy will return an empty array, []
    elif (type(pingStatus).__name__ == 'list'):
        # It will threat as request timeout
        return 408
    else:
        return ''
  
  def check_tor_status():
    pingStatus = Tor.proxy_request(STATIC_URL, DOMAIN_REQUEST)
    if (pingStatus == TOR_SERVICE_DOWN):
      print(TOR_SERVICE_DOWN)
      raise HTTPException(404, "Tor service down")
    return 200
