from django.conf.urls import url, include


urlpatterns = [
    url(r'^api/', include('cmdb_api.urls', namespace='api', app_name='cmdb_api')),
    url(r'^', include('cmdb_ui.urls', namespace='cmdb', app_name='cmdb_ui'))
]
