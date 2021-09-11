import os
import sys

webname = sys.argv[1]
website_name="pywebbuilder.in"
site_apache_conf="/etc/apache2/sites-available/%s.conf"%webname
home_dir = "/var/www/"
gmail = "pywebbuilder@gmail.com"


apache_conf = """<VirtualHost *:80>
		ServerName %s
		ServerAdmin %s
		WSGIScriptAlias / /var/www/FlaskApp/flaskapp.wsgi
		<Directory /var/www/FlaskApp/FlaskApp/>
			Order allow,deny
			Allow from all
		</Directory>
		Alias /static /var/www/FlaskApp/FlaskApp/static
		<Directory /var/www/FlaskApp/FlaskApp/static/>
			Order allow,deny
			Allow from all
		</Directory>
		ErrorLog ${APACHE_LOG_DIR}/error.log
		LogLevel warn
		CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
""" %(website_name, gmail)


flaskapp_wsgi = """#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/FlaskApp/")

from FlaskApp import app as application
application.secret_key = \'test\'
""".replace("FlaskApp",webname)
apache_conf = apache_conf.replace("FlaskApp",webname)

cmds = ["sudo apt update","sudo apt install apache2","sudo apt-get install libapache2-mod-wsgi python3-dev","sudo apt-get install libapache2-mod-wsgi-py3",
        "sudo a2enmod wsgi", "mkdir -p %s/%s/%s/templates"%(home_dir,webname,webname),"mkdir -p %s/%s/%s/static"%(home_dir,webname,webname),
        "sudo apt-get install python3-pip","sudo pip3 install virtualenv","sudo virtualenv venv","sudo pip3 install Flask",
        "echo '%s'>%s"%(apache_conf,site_apache_conf), "sudo a2ensite %s"%webname,
        "echo '%s'>%s" %(flaskapp_wsgi,"/var/www/%s/flaskapp.wsgi"%webname),"sudo service apache2 restart "
        
        "sudo add-apt-repository ppa:certbot/certbot","sudo apt install python3-certbot-apache","certbot -d www.%s -d %s"%(website_name,website_name),"sudo service apache2 restart","sudo systemctl reload apache2"


        ]
for cmd in cmds:
    os.system(cmd)
