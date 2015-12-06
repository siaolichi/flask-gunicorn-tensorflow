FROM python:3.4.3

RUN apt-get update
RUN apt-get -y install nginx uwsgi-plugin-python3 supervisor

RUN mkdir /app

# uwsgi setup
COPY uwsgi.ini /app/

# nginx setup
RUN rm /etc/nginx/sites-enabled/default
COPY nginx.conf /etc/nginx/sites-available/flask.conf
RUN ln -s /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled/flask.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# supervisor setup
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# copy sample project
COPY app /app
RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["/usr/bin/supervisord"]

VOLUME /app
EXPOSE 80
