#!/bin/bash
# Author: Alastair Kerr
# Spin up infrastructure with docker
# Create docker images from Dockerfiles, runs containers

YELLOW='\033[0;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# If true, delete all existing OFC images/ containers and rebuild from scratch
FORCE=false 
# If passed an IP address as arg use this for database config options for OFCP service 
IP_SET=false
# If no IP is provided, default behaviour is to not change the IP set in OFCP/src/config.py
DEFAULT_USE_CONFIG_IP=true

# Container names
OFC_SVC="ofc-service"
OFC_SQL="ofc-sql"
OFC_DATA_VOL="ofc-sql-data"

# Image names
OFC_SVC_IMG="ofc-service-image"
OFC_SQL_IMG="ofc-sql-image"
OFC_DATA_IMG="ofc-sql-data-image"

function usage {
    echo -e "${YELLOW}Usage: -a (autodetect host IP) -i <host IP> -f (force rebuild) -t (teardown only) -h (help)${NC}"
}

function teardown {
    echo -e "${YELLOW}Tearing down existing images/ containers..${NC}"
    docker rm -f ${OFC_SVC} ${OFC_SQL} ${OFC_DATA_VOL}
    docker rmi -f ${OFC_SVC_IMG} ${OFC_SQL_IMG} ${OFC_DATA_IMG} 
}

while [[ $# > 0 ]]
do
flag="$1"
case $flag in
    -a|--autodetect)
    DEFAULT_USE_CONFIG_IP=false
    ;;
    -f|--force)
    FORCE=true
    ;;
    -h|--help)
    usage && exit 0
    ;;
    -i|--ip)
    IP_SET=true
    HOST_IP="$2"
    if ! [[ "${HOST_IP}" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
      echo -e "${RED}Invalid IPv4 address '${HOST_IP}'${NC}"
      usage && exit 1
    fi
    shift
    ;;
    -t|--teardown)
    teardown && exit 0
    ;;
    *)
    echo -e "${RED}Unknown flag `echo $flag | tr -d '-'`${NC}" && usage && exit 1
esac
shift
done

# Print info about interpreted command line arguments  
echo -e "${YELLOW}Force rebuild: ${FORCE}${NC}"
echo -e "${YELLOW}Using provided IP address: ${IP_SET}${NC}"
if [ "${IP_SET}" = true ]; then
    echo -e "${YELLOW}Provided IP address: ${HOST_IP}${NC}"
else
    if [ "${DEFAULT_USE_CONFIG_IP}" = false ]; then
        AUTO_DETECT=true
    else
        AUTO_DETECT=false
    fi
    echo -e "${YELLOW}Auto-detect host IP: ${AUTO_DETECT}${NC}"
fi

if [ "${FORCE}" = true ]; then
    teardown
fi

echo -e "${YELLOW}Spawning OFC infrastructure..${NC}"

# Database Data Container - Build image if necessary, and spawn container
docker images | grep -q ${OFC_DATA_IMG}
if [ $? -eq 0 ]; then
    echo -e "${YELLOW}Using existing docker image for ofc-sql-data container${NC}"
else
    echo -e "${YELLOW}Building new image for ofc-sql-data container${NC}"
    ( cd mysql-data && docker build --no-cache -t ${OFC_DATA_IMG} . )
fi
docker run -dit --name ${OFC_DATA_VOL} ${OFC_DATA_IMG}

# Database Service Container - Build image if necessary, and spawn container
docker images | grep -q ${OFC_SQL_IMG}
if [ $? -eq 0 ]; then
    echo -e "${YELLOW}Using existing docker image for ofc-sql container${NC}"
else
    echo -e "${YELLOW}Building new image for ofc-sql container${NC}"
    ( cd mysql && docker build --no-cache -t ${OFC_SQL_IMG} . )
fi
docker run --privileged --volumes-from ${OFC_DATA_VOL} -dit --name ${OFC_SQL} -p 3306:3306 ${OFC_SQL_IMG}

# OFCP Service Container - Build image if necessary, and spawn container
docker images | grep -q ${OFC_SVC_IMG}
if [ $? -eq 0 ]; then
    echo -e "${YELLOW}Using existing docker image for ofc-service container${NC}"
else
    echo -e "${YELLOW}Building new image for ofc-service container${NC}"
    if [ "${IP_SET}" = true ]; then
        echo "${HOST_IP}" > ofc/files/host_ip
    elif [ "${DEFAULT_USE_CONFIG_IP}" = false ]; then
        HOST_IP=$(ip route get 1 | awk '{print $NF;exit}')
        if [ $? -eq 0 ]; then
            echo "${HOST_IP}" > ofc/files/host_ip
        else
            echo -e "${RED}Failed to autodetect IP, exiting..${NC}" && exit 1
        fi
    fi
    ( cd ofc && docker build --no-cache -t ${OFC_SVC_IMG} . )
    ls ofc/files/host_ip > /dev/null 2>&1 && rm -f ofc/files/host_ip
fi
docker run -dit --name ${OFC_SVC} -p 8080:8080 ${OFC_SVC_IMG}
