FROM python:3.4.3

RUN apt-get update
RUN apt-get -y install nginx supervisor
RUN pip install --no-cache-dir gunicorn

RUN mkdir -p /data
COPY app /data
RUN pip install --no-cache-dir -r /data/requirements.txt
VOLUME ["/data", "/var/log"]

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
