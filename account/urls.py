from django.urls import path, include
from account.views import Register
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', Register.as_view(), name='register'),
    path('home/', views.lk, name='lk'),
    path('logout/', views.mylogout, name='logout'),
    path('boost/', views.boost, name='boost'),
    path('makeapplicate', views.applicate, name='makeapplicate'),
]
