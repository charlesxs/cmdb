from django.conf.urls import url
from .views import login, index


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login/$', login, name='login')
]