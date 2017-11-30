from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from urllib.request import urlopen, urlretrieve
from urllib.error import HTTPError
from traitlets.config import Config
from nbconvert import HTMLExporter
from hashlib import md5

import os, pwd, sys
import nbformat

def login(request):
    return render(request, 'upload/login.html')

extensions = ['.ipynb', '.scala']

#@login_required
def preview(request, notebook_url):
    try:
        notebook_response = urlopen(notebook_url).read().decode()
        if notebook_url.endswith('.ipynb'):
            html_exporter = HTMLExporter()
            html_exporter.template_file = 'full'
            notebook_data = nbformat.reads(notebook_response, as_version=4)
            (body, resources) = html_exporter.from_notebook_node(notebook_data)
            context = {
                'notebook_url':     notebook_url,
                'notebook_preview': body,
            }
            return render(request, 'upload/preview.html', context)
        else:
            context = {
                'notebook_url':     notebook_url,
                'notebook_preview': '<pre>' + notebook_response + '</pre>',
            }
            return render(request, 'upload/preview.html', context)

    except HTTPError as error:
        context  = {
            'notebook_url':     notebook_url,
            'error_msg':        error,
        }
        return render(request, 'upload/preview_error.html', context)

@login_required
def index(request):
    matches  = [p for p in pwd.getpwall() if p.pw_name == request.user.username]
    nmatches = len(matches)
    # NO USER
    if nmatches != 1:
        return render(request, 'upload/nouser.html')
    else:
        return render(request, 'upload/index.html')
    
@login_required
def confirm(request, notebook_url):
    matches  = [p for p in pwd.getpwall() if p.pw_name == request.user.username]
    nmatches = len(matches)
    # NO USER
    if nmatches != 1:
        return render(request, 'upload/nouser.html')
    # UNSUPPORTED FILE EXTENSION

    if not notebook_url.endswith(tuple(extensions)):
        context  = {
            'notebook_url': notebook_url,
        }
        return render(request, 'upload/error.html', context)
    # CONFORMATION PAGE
    salt     = 'upload.aods.io'
    token    = md5((notebook_url + salt).encode()).hexdigest()
    secret   = md5((token + salt).encode()).hexdigest()
    context  = {
        'notebook_url':     notebook_url,
        'upload_token':     token,
    }
    resp = render(request, 'upload/confirm.html', context)
    resp.set_cookie('secret', secret)
    return resp

@login_required    
def upload(request, upload_token, notebook_url):

    matches  = [p for p in pwd.getpwall() if p.pw_name == request.user.username]
    nmatches = len(matches)
    
    salt   = 'upload.aods.io'
    secret = request.COOKIES.get('secret')
    actual = md5((upload_token + salt).encode()).hexdigest()

# todo    
#    if secret != actual:
#        return render(request, 'upload/upload_error.html')
        
    # POST-UPLOAD PAGE
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    notebook_filename = notebook_url.rsplit('/', 1)[-1]
    if notebook_url.endswith('.ipynb'):
        notebook_filename = notebook_filename[:-6] + '.' + timestamp + '.ipynb'
    else:
        notebook_filename = notebook_filename
    notebook_path     = matches[0].pw_dir + '/' + notebook_filename

    #local_filename, headers = urlretrieve(notebook_url, notebook_path) # need to replace with urlopen and write    
    #os.chown(path, matches[0].pw_uid, matches[0].pw_gid)

    with urlopen(notebook_url) as notebook_response:
        notebook_bytes = notebook_response.read()
        with open(notebook_path, 'wb') as wfile:
            wfile.write(notebook_bytes)
        os.chown(notebook_path, matches[0].pw_uid, matches[0].pw_gid)    
    
    context  = {
        'notebook_url': notebook_url,
        'user_home': matches[0].pw_dir,
        'notebook_filename': notebook_filename,
        'nmatches': nmatches,
        'matches': matches,
        'secret': secret,
        'actual': actual,
    }
    
    return render(request, 'upload/upload.html', context)


        
        

