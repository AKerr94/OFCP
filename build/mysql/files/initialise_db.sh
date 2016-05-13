#!/bin/bash
# Initialise MySQL database

service mysql start &
mysql_pid=$!

until mysqladmin ping &>/dev/null; do
	echo -n "."; sleep 0.2
done

mysql < /tmp/create_ofc_db.sql
