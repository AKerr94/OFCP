FROM ubuntu
MAINTAINER Alastair Kerr

RUN export DEBIAN_FRONTEND=noninteractive
RUN apt-get -q -y install mysql-server

RUN mkdir -p /var/lib/ofc/init
ADD files/* /var/lib/ofc/init/
RUN /var/lib/ofc/init/initialise_db.sh
RUN cp /var/lib/ofc/init/ofc-sql-start /usr/bin/ofc-sql-start

CMD ofc-sql-start
