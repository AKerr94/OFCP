#!/bin/bash
# Initialise MySQL database

mysql_install_db
/usr/sbin/mysqld
mysql_pid=$!

until mysqladmin ping &>/dev/null; do
	echo -n "."; sleep 0.2
done

mysql -ppassword < /tmp/create_ofc_db.sql
