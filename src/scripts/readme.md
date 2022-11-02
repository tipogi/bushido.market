When `Tor` service all the time start ups, it creates a new circuit, new identity. For privacy reason, to not make request always from the same circuit, we are going to restart after some time.

### Configuration
First make executable our script
```bash
chmod +x restart_tor_circuit.sh
```
To restart periodically the docker service (tor-proxy), we are going to add a cron job. In our case, we want to restart each 6 hours. More info [here](https://crontab.guru/every-6-hours)
```bash
# Edit the crontab file
crontab -e
# Add the script that we want to execute and the execution time
# At minute 0 past every 6th hour
0 */6 * * * ~/www/bushido/bushido.deploy/docker/bushido.market/src/scripts/restart_tor_circuit.sh
# Check our crontab if it was add 
crontab -l
```

### Notifications
Notifications will be located in /var/spool/mail in `bushido` file