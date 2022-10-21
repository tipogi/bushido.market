docker container ls  | grep 'tor-proxy' | awk '{print $1}'
# Restart docker container
docker container ls  | grep 'tor-proxy' | awk '{ system("docker restart " $1) }'