#!/bin/bash
# Initialise MySQL database

service mysql start &
mysql_pid=$!

until mysqladmin ping &>/dev/null; do
	echo -n "."; sleep 0.2
done

# Variables used for setting ofcdatabaseuser password and IP to access from
PASSWORD="password"
DOCKER_IP=$(ifconfig | grep -A1 docker0 | tail -n 1 | awk '{print $2}')

# Customise sql commands from variables above
sed "s/password/${PASSWORD}/g" /tmp/create_ofc_db.sql.template | \
sed "s/dockerip/${DOCKER_IP}/g" > /tmp/create_ofc_db.sql
mysql < /tmp/create_ofc_db.sql
