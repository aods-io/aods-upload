from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^preview/(?P<notebook_url>.*)$', views.preview, name='preview'),
    url(r'^upload/(?P<upload_token>[a-f0-9]+)/(?P<notebook_url>.*)$', views.upload, name='upload'),
#    url(r'^success/(?P<notebook_name>.*)$', views.success, name='success'),    
    url(r'^oauth/', include('social_django.urls', namespace='social')),  # <--
    url(r'^admin/', admin.site.urls),
    url(r'^(?P<notebook_url>.*)$', views.confirm, name='confirm'),            
]
