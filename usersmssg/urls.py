from django.conf.urls import url
from . import views

# We are adding a URL called /home
urlpatterns = [
    url(r'^mssg/$', views.mssg_all_page, name='mssg_all_page'),
    url(r'^mssg/from/(?P<user>[0-9]+)/$', views.mssg_from_page, name='mssg_from_page'),
    url(r'^mssg/to/(?P<user>[0-9]+)/$', views.mssg_to_page, name='mssg_to_page'),
    url(r'^mssg/write/$', views.mssg_write, name='mssg_write'),
    url(r'^mssg/jquery/mssg_get_inbox/$', views.mssg_get_inbox, name='mssg_get_inbox'),
]
