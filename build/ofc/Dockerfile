FROM ubuntu:latest
MAINTAINER ake31 <alastair.kerr@sky.uk>

RUN apt-get install -q -y git python python-MySQLdb wget
RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py
RUN pip install cherrypy jinja2 MySQL-python
RUN cd /opt && git clone https://github.com/AKerr94/OFCP.git

CMD cd /opt/OFCP/src && python server.py
