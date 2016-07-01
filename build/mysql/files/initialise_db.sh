#!/bin/bash
# Initialise MySQL database

CONFIG_DIR=/var/lib/ofc/init
source ${CONFIG_DIR}/config

service mysql start &
mysql_pid=$!

until mysqladmin ping &>/dev/null; do
	echo -n "."; sleep 0.2
done

# Query docker IP that mysql access requests come from
DOCKER_IP=$(ifconfig | grep -A1 docker0 | tail -n 1 | awk '{print $2}')

# Customise sql commands from variables above
sed "s/password/${DB_PASSWORD}/g" ${CONFIG_DIR}/create_ofc_db.sql.template | \
sed "s/dockerip/${DOCKER_IP}/g" > ${CONFIG_DIR}/create_ofc_db.sql
mysql < ${CONFIG_DIR}/create_ofc_db.sql
