#!/bin/bash
# Spin up infrastructure with docker
# Create docker images from Dockerfiles, runs containers

cd mysql 
docker build --no-cache -t ofc-sql-image .
docker run -it -d --name test ofc-sql-image /bin/bash
