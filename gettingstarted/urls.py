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
    url(r'^logout/$', 'hello.views.logout_view'),
    url(r'^register/$', 'hello.views.register'),
    url(r'^register/success/$', 'hello.views.success'),
    url(r'^landing/$', 'hello.views.landing'),
    url(r'^bookOwner/(?P<owner>[a-zA-Z0-9_]+)$', 'hello.views.bookOwner'),
    url(r'^landing/(?P<book>[0-9]+)$', 'hello.views.showBook'),
    url(r'^landing/(?P<reserve>[0-9]+)/deleteReserve/$', 'hello.views.delReserve'),
    url(r'^landing/addBook/$', 'hello.views.addBook'),
    url(r'^landing/(?P<book>[0-9]+)/addReserve/$', 'hello.views.addReserve'),
    url(r'^landing/(?P<book>[0-9]+)/editResource/$', 'hello.views.editResource'),
    url(r'^(?P<book>[0-9]+)/rssFeed$', 'hello.views.rssFeed'),
    url(r'^landing/(?P<tagid>[0-9]+)/showTag$', 'hello.views.showTag'),

    #url(r'^logout/$', 'django.contrib.auth.views.logout'),
    #url(r'^db', hello.views.db, name='db'),
    #url(r'^admin/', include(admin.site.urls)),

)
