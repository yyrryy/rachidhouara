from django.urls import path

from . import views

urlpatterns=[
    path('', views.account, name='account'),
    path('garage', views.garage, name='garage'),
    path('editprofile', views.editprofile, name='editprofile'),
    path('orders', views.orders, name='orders'),
    path('addresses', views.addresses, name='addresses'),
    path('editaddress', views.editaddress, name='editaddress'),
    path('password', views.password, name='password'),
]
