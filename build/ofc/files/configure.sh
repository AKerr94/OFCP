#!/bin/bash
# Runs necessary configuration for OFCP service
ls /var/lib/ofc/init/host_ip > /dev/null 2>&1 
if [ $? -eq 0 ]; then
	HOST_IP=$(cat /var/lib/ofc/init/host_ip)
	sed -i "s/.*'HOST':.*/    'HOST': '${HOST_IP}',/" /opt/OFCP/src/config.py
fi
