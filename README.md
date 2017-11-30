# aods-upload

The AODS Upload project is comprised primarily of a web application that facilitates the automatic uploading of notebooks to a JupyterHub workspace. 
Features include: i) social authentication; ii) rendering notebook previews; iii) and linking a user directly to the uploaded notebook in their AODS JupyterHub workspace. 
Written in Python using the Django library, the application is designed to perform a minimal set of operations while maintaining a small footprint on the system.
Its functionality and implementation are directly motivated by and adhere to the [AODS Guidelines](http://aods.io/#aods-guidelines).

A proof of concept installation is hosted at [`aods.io`](http://aods.io), primarily targeted at readers of Michael E. Cotterell's Ph.D. dissertation. 
The AODS Upload software and documentation are free and open source under an MIT license and Creative Commons license, respectively. 

## Social Authentication

The AODS Upload application uses GitHub accounts to authenticate users using the [`social-auth-app-django`](hhttps://github.com/python-social-auth/social-app-django) package.
Install this package following the instructions found [here](https://github.com/python-social-auth/social-app-django).
Next, setup an OATH App on GitHub following the instructions found [here](https://developer.github.com/apps/building-integrations/setting-up-and-registering-oauth-apps/registering-oauth-apps/).
If you have an existing OATH App registered for your JupyterHub installation, then you will need to make a new one for this application since the callback URL will be different. 
This will give you the information you need to fill out client information below.
Now, add the following settings to the `upload_site/secret_settings.py` file (create it if it does not exist):

```python
SECRET_SETTINGS_SOCIAL_AUTH_URL_NAMESPACE = 'social'
SECRET_SETTINGS_SOCIAL_AUTH_GITHUB_KEY = ''
SECRET_SETTINGS_SOCIAL_AUTH_GITHUB_SECRET = ''
```

## Configure Additional Settings

You will need to configure the following additional settings to the `upload_site/secret_settings.py` file (create it if it does not exist):

```python
SECRET_SETTINGS_SECRET_KEY = ''
SECRET_SETTINGS_DEBUG = False
SECRET_SETTINGS_ALLOWED_HOSTS = ['']
SECRET_SETTINGS_STATIC_URL = '/static/'
SECRET_SETTINGS_STATIC_ROOT = "/path/to/static/"
```

Each of the settings above is a Django setting with `SECRET_SETTINGS_` prefixed.
See Django's [documentation](https://docs.djangoproject.com/en/1.11/topics/settings/) for more details.

## Deployment with uWSGI and Nginx

The AODS Upload application can be deployed using the [uWSGI](http://uwsgi-docs.readthedocs.io/en/latest/) package.
Install this package following the instructions found [here](http://uwsgi-docs.readthedocs.io/en/latest/Install.html).

Here is an example that starts the application locally on port 8888.

```
$ uwsgi --http :8888 \
        --chdir /path/to/aods-upload/upload_site \
        --wsgi-file /path/to/aods-upload/upload_site/upload_site/wsgi.py \
        --virtualenv /path/to/aods-upload
```

If you are using the Nginx webserver, then you can use an Nginx configuration similar to the following to proxy port 80 for a particular hostname (replace `hostname.tld`) so that it forwards to the AODS Upload application that is running locally on port 8888:

```
server {
	listen 80;
	server_name hostname.tld;
	client_max_body_size 75M;

	location /static/ {
		alias /path/to/static/;
		gzip_static on;
		expires max;
		add_header Cache-Control public;		
	}

	location / {
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_pass http://127.0.0.1:8888;
	}

}
```

Instructions for Apache2 are coming soon!

<hr>
<small>
<p><a href="https://creativecommons.org/licenses/by-sa/4.0/"><img src="https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg" alt="License: CC BY-SA 4.0" /></a></p>
<p>Copyright 2017 Michael E. Cotterell (mepcott@uga.edu) and the University of Georgia. The documentation fot this work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>. The software projects described here may be subject to their own licenses. The content and opinions expressed on this Web page do not necessarily reflect the views of nor are they endorsed by the University of Georgia or the University System of Georgia.</p>
</small>
