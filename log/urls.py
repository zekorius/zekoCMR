from django.conf.urls import url
from . import views

# We are adding a URL called /home
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'home$', views.home, name='home'),
    url(r'companies$', views.companies_page, name='companies_page'),
    url(r'users$', views.users_page, name='users_page'),
    url(r'test$', views.strona_testowa, name='strona_testowa'),
]