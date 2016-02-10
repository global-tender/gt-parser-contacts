
```
Developed using Python 2.7, Django 1.9.1
Database is SQLite
```

### Requires:
```
python2
python3
python-pip
python3-pip
pip3 install XlsxWriter
python-dev
```

### Set up virtualenv, ex (using virtualenvwrapper):

```
$ pip install virtualenvwrapper
...
$ export WORKON_HOME=~/Envs
$ mkdir -p $WORKON_HOME
$ source /usr/local/bin/virtualenvwrapper.sh
$ mkvirtualenv --system-site-packages zakupki
$ workon zakupki

# enter repository root directory and install other required python packages:
$ pip install -r requirements.txt
```

### Finish work with django
 * Initialize database:

```
python manage.py makemigrations
python manage.py makemigration org_manager
python manage.py migrate
python manage.py migrate org_manager
```

### Setup Production (using nginx + gunicorn)
All-sufficient guide: http://goodcode.io/blog/django-nginx-gunicorn/

Running gunicorn (WSGI HTTP Server) this way (3 instances, max timeout 1000 seconds):

```
gunicorn system.wsgi -w 3 -t 1000 --log-file=/path/to/gunicorn.log -b 127.0.0.1:8181
```

Nginx config for our virtual host (replace PATH where needed):

```
server {
        listen 80;
        client_max_body_size 100M;
        server_name zakupki.global-tender.ru;
        access_log /path/to/access.log;
        error_log /path/to/error.log;

        root /path/to/our/django/site/app_name/;

        location /static/ { # STATIC_URL
                alias /path/to/our/primary/application/static/; # STATIC_ROOT
                expires 30d;
        }

        location / {
                proxy_pass_header Server;
                proxy_set_header Host $http_host;
                proxy_redirect off;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Scheme $scheme;
                proxy_connect_timeout 180;
                proxy_read_timeout 1000;
                proxy_pass http://127.0.0.1:8181/;
        }
}
```

### Setup cron task for user which run site:

SHELL=/bin/bash
WORKON_HOME=~/Envs

0 0 * * 5 source /usr/local/bin/virtualenvwrapper.sh && workon zakupki && cd <full path to repository root directory> && python manage.py flow