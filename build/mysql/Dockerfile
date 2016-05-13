FROM ubuntu
MAINTAINER Alastair Kerr

RUN export DEBIAN_FRONTEND=noninteractive
RUN apt-get -qy install mysql-server

ADD files/* /tmp/
RUN /tmp/initialise_db.sh
