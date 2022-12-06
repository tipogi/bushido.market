# Bushido Market API
**BIG THANKS** to *Barney Buffet* and *j4imefoo* for their awesome repositories that helps to create that. The creation of that, is a fusion of two repositories.
Instead of making requests from the CLI, we have an API server to make queries against that. After, all the queries are proxied through the tor service.
- [Docker Tor](https://github.com/BarneyBuffet/docker-tor): A docker image that runs a Tor service on an Alpine linux base image
- [nokyc](https://github.com/j4imefoo/nokyc): A script that lists all current Bisq, HodlHodl, Robosats and LNP2PBot offers in the terminal

## Overview

![Market Architecture](./docs/assets/nest-clean-architecture.png)

Clients interacts with the system through the API-Gateway. The market module executes the corresponding use-case and proxies the request through the proxy server. Usually, all the requests that travel through the tor network are going to different P2P exchanges (API) as Hodl Hold, Bisq, P2PLNBot and RoboSats to get the market offers.
That two modules, work in top of a docker containers which gives the flexibility to be more portable and be able to install in a place that we want.

## Containers Network
Create a docker network to set the communication between the containers. Even docker creates a default network in each docker-compose execution, in `torrc` file, we cannot use docker container name becase it breaks the naming pattern, it has to be an IP.
Allow to the **app container** to make request against the tor **proxy container** editing the default value of `TOR_PROXY_ACCEPT`. Docker proxy container does not expose its SOCKS port to outside, it is just accessible from inside of the docker network.
The below variables would be the default ones but we can add also the following Tor flags (next block). Once we add in the `.env` new variables, we have to add that flags as `environments` key in the `docker-compose.yml` file.
```yaml
NETWORK_SUBNET=10.0.0.0/8
TOR_STATIC_IP=10.0.0.1
APP_STATIC_IP=10.0.0.2
TOR_PROXY_ACCEPT="accept 127.0.0.1,accept ${APP_STATIC_IP}"
```
## Tor Proxy Environmental Flags

Below is a list of available environmental flags that can be set during container creation.

| Flag | Choices/Default | Comments |
|:-----|:----------------|:---------|
| TOR_CONFIG_OVERWRITE | true/__false__ | Create new torrc file each time we spin up the container |
| TOR_LOG_CONFIG | true/__false__ | Should the tor config file `torrc` be echo'd to the log. This can be helpful when setting up a new Tor daemon |
| TOR_PROXY      | __true__/false | Set up the Tor daemon as a Socks5 proxy |
| TOR_PROXY_PORT | string (__9050__) | What port the Tor daemon should listen to for proxy requests |
| TOR_PROXY_SOCKET| true/__false__ | Create a unix socket for the proxy in the data folder |
| TOR_PROXY_ACCEPT | __accept 127.0.0.1__ | What IP addresses are allowed to route through the proxy |
| TOR_CONTROL | true/__false__ | Should the Tor control be enabled |
| TOR_CONTROL_PORT | string | What port should the Tor daemon be controlled on. If enabled cookie authentication is also enabled by default |
| TOR_CONTROL_SOCKET | true/false | Create a unix socket for the Tor control |
| TOR_CONTROL_PASSWORD | string | Authentication password for using the Tor control port |
| TOR_CONTROL_COOKIE | true/false | Cookie to confirm when Tor control port request sent |
| TOR_SERVICE | true/__false__ | Set up the Tor daemon with hidden services |
| TOR_SERVICE_HOSTS | hostname=wan-port:redict-ip:rediect-port | Tor hidden service configuration |
| TOR_SERVICE_HOSTS_CLIENTS | hostname:client-1,client-2,... | Authorised clients for hostname |
| TOR_RELAY | true/__false__ | ** NOT IMPLEMENTED YET ** |

## IMPORTANT
- When we change the configuration files delete the volume of tor

## Resources
- [Docker Tor docs](https://barneybuffet.github.io/docker-tor/)
- [Running Tor proxy with docker](https://dev.to/nabarun/running-tor-proxy-with-docker-56n9)
- [How to use Python with Tor and Privoxy](https://gist.github.com/DusanMadar/8d11026b7ce0bce6a67f7dd87b999f6b)
- [torpool](https://github.com/u1234x1234/torpool)
- [Asynchronous http request in python with aiohttp](https://www.twilio.com/blog/asynchronous-http-requests-in-python-with-aiohttp)
- [Speeding Up Python with Concurrency, Parallelism, and asyncio](https://testdriven.io/blog/concurrency-parallelism-asyncio/)
- [Configure Tor as a listening proxy server that I can connect to remotely?](https://superuser.com/questions/458491/configure-tor-as-a-listening-proxy-server-that-i-can-connect-to-remotely)
- [Cannot get tor proxy to work](https://forum.openwrt.org/t/cant-get-tor-socks-proxy-to-work/64142)