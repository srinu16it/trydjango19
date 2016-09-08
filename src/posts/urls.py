from django.conf.urls import url
from django.contrib import admin
#from posts import views
from . import views
#from accounts.views import login_view
#from accounts.views import (login_view, register_view, logout_view)


urlpatterns = [
    url(r'^$', views.post_list,name='list'),
    url(r'^create/$', views.post_create),
    url(r'^(?P<slug>[-\w]+)/$', views.post_detail,name='detail'),
    url(r'^(?P<slug>[-\w]+)/edit/$', views.post_update,name='update'),
    url(r'^(?P<slug>[-\w]+)/delete/$', views.post_delete),
    



    #url(r'^posts/$', "posts.views.post_home"),
    #url(r'^posts/$', "<appname>views.<Function name>"),
]
#url(r'^(?P<slug>[-\w]+)/$', Display.as_view(), name="get_post"),

#url(r'^posts/$', views.post_home),
#url(r'^admin/', admin.site.urls),
