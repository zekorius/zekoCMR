from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^categories/$', views.categories_page, name='categories_page'),
]
