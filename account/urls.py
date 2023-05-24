from django.urls import path, include
from account.views import Register
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', Register.as_view(), name='register'),
    path('home/', views.lk, name='lk'),
    path('logout/', views.mylogout, name='logout'),
    path('boost/', views.boost, name='boost'),
    path('makeapplicate/', views.applicate, name='make_application'),
    path('boost/', views.boost, name='boost'),
    path('takeorder/', views.take_order, name='take_order'),
    path('seeapplications/', views.see_applications, name='see_applications'),
    path('myorders', views.my_orders, name='my_orders'),
    path('myboughtorders', views.bought_orders, name='bought_orders'),
]
