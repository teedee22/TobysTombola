Provisioning a new site
=======================
eg, on Ubuntu:

sudo ufw allow OpenSSH
sudo sudo ufw status
sudo apt-get update && apt-get upgrade
sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx

sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv

    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install nginx git python36 python3.6-venv

## Nginx Virtual Host config

* see nginx.template.conf
* replace DOMAIN with, e.g., staging.my-domain.com

cat ./deploy_tools/nginx.template.conf \
    | sed "s/DOMAIN/pop22.westeurope.cloudapp.azure.com/g" \
    | sudo tee /etc/nginx/sites-available/pop22.westeurope.cloudapp.azure.com

    sudo ln -s /etc/nginx/sites-available/pop22.westeurope.cloudapp.azure.com \
    /etc/nginx/sites-enabled/pop22.westeurope.cloudapp.azure.com

## Systemd service

* see gunicorn-systemd.template.service
* replace DOMAIN with, e.g., staging.my-domain.com

cat ./deploy_tools/gunicorn-systemd.template.service \
    | sed "s/DOMAIN/pop22.westeurope.cloudapp.azure.com/g" \
    | sudo tee /etc/systemd/system/pop22.westeurope.cloudapp.azure.com.service

cat ./deploy_tools/gunicorn.systemd.template.socket \
    | sed "s/DOMAIN/pop22.westeurope.cloudapp.azure.com/g" \
    | sudo tee /etc/systemd/system/pop22.westeurope.cloudapp.azure.com.socket

sudo systemctl daemon-reload
sudo systemctl reload nginx
sudo systemctl enable pop22.westeurope.cloudapp.azure.com
sudo systemctl start pop22.westeurope.cloudapp.azure.com
sudo systemctl restart nginx
sudo ufw allow 'Nginx Full'

## Folder structure:

Assume we have a user account at /home/username

/home/username
└── sites
    ├── DOMAIN1
    │    ├── .env
    │    ├── db.sqlite3
    │    ├── manage.py etc
    │    ├── static
    │    └── virtualenv
    └── DOMAIN2
         ├── .env
         ├── db.sqlite3
         ├── etc
