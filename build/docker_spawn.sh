#!/bin/bash
# Spin up infrastructure with docker
# Create docker images from Dockerfiles, runs containers

docker images | grep -q ofc-sql-image
if [ $? -eq 0 ]; then
    echo "Building new image for ofc-sql container"
    ( cd mysql && docker build --no-cache -t ofc-sql-image . )
else
    echo "Using existing docker image for ofc-sql container"
fi
docker run -it -d --name ofc-sql-test -p 3306:3306 ofc-sql-image /bin/bash
