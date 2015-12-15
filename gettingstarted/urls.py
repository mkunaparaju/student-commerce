from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login
from django.contrib.auth.views import logout

from django.contrib import admin
admin.autodiscover()

import hello.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gettingstarted.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^$', hello.views.index),
    #url(r'^$', hello.views.login_user, name='login_user'),
    url(r'^$', 'hello.views.login_user'),
    url(r'^landing/$', 'hello.views.landing'),
    #url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),

)
