from proxy.tor import Tor, DOMAIN_REQUEST

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
