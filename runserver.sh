#!/bin/bash

cd /root/Beta/
touch /root/sdfz
echo 'yes' | python3 manage.py collectstatic
nginx
uwsgi --ini Beta_uwsgi.ini
