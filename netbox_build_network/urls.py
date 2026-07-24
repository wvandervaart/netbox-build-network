from django.urls import path

from . import views

app_name = 'netbox_build_network'

urlpatterns = [
    path('build/', views.BuildnwRedirectView.as_view(), name='build_network'),
]