from os import name
from django.urls import path
from . import views
from .views import ( DashboardAPIView, RegistrationAPIView , LoginAPIView )

app_name = 'authentication'
urlpatterns = [
    path('',views.home,name="home"),
    path('user_registration/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('dashboard/',DashboardAPIView.as_view()),
]



