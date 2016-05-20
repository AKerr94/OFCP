FROM ubuntu
MAINTAINER Alastair Kerr

RUN export DEBIAN_FRONTEND=noninteractive
RUN apt-get -q -y install mysql-server
#RUN mysqladmin -u root password pw123

ADD files/* /tmp/
RUN /tmp/initialise_db.sh
RUN cp /tmp/ofc-sql-start /usr/bin/ofc-sql-start

CMD ofc-sql-start
