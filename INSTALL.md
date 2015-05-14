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
$ mkvirtualenv --system-site-packages gt_parser_contacts
$ workon gt_parser_contacts

# enter repository root directory and install other required python packages:
$ pip install -r requirements.txt
```

### Finish work with django
 * Initialize database (this will create all tables). You'll get a prompt asking you if you'd like to create a superuser account for the authentication system. Go ahead and do that:

```
python manage.py syncdb
```

### Setup Production (using nginx + gunicorn)
All-sufficient guide: http://goodcode.io/blog/django-nginx-gunicorn/

Running gunicorn (WSGI HTTP Server) this way (3 instances, max timeout 180 seconds):

```
gunicorn systemTool.wsgi -w 3 -t 1000 --log-file=/path/to/gunicorn.log -b 127.0.0.1:8181
```

Nginx config for our virtual host (replace PATH where needed):

```
server {
        listen 80;
        client_max_body_size 100M;
        server_name gtpc.ihptru.net;
        access_log /path/to/access.log;
        error_log /path/to/error.log;

        root /path/to/our/django/site/;
        location /static/ { # STATIC_URL
                alias /path/to/our/primary/application/static/; # STATIC_ROOT
                expires 30d;
        }

        location /media/ { # MEDIA_URL
                alias /path/to/our/primary/application/static/; # MEDIA_ROOT
                expires 30d;
         }
        location /static/admin/ {
                alias /usr/local/lib/python2.7/dist-packages/django/contrib/admin/static/admin/;
        }
        location / {
                proxy_pass_header Server;
                proxy_set_header Host $http_host;
                proxy_redirect off;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Scheme $scheme;
                proxy_connect_timeout 30;
                proxy_read_timeout 1000;
                proxy_pass http://127.0.0.1:8181/;
        }
}
```
