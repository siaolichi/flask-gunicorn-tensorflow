FROM python:3.6

MAINTAINER Nicolas Allemand <contact@nicolasallemand.com>

RUN apt-get update
RUN apt-get -y install nginx supervisor python3-pip python3-dev
RUN pip install --no-cache-dir gunicorn Flask tensorflow tflearn 

RUN mkdir -p /usr/src/app
RUN mkdir -p /usr/src/app/static
WORKDIR /usr/src/app

ONBUILD COPY requirements.txt /usr/src/app/
ONBUILD RUN pip install --no-cache-dir -r requirements.txt

ONBUILD COPY . /usr/src/app

# nginx setup
RUN rm /etc/nginx/sites-enabled/default
COPY flask.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled/flask.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# supervisor setup
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/
COPY gunicorn.conf /etc/supervisor/conf.d/

EXPOSE 80
CMD ["/usr/bin/supervisord"]
