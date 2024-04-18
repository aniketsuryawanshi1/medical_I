from django.urls import path
from app import views


urlpatterns = [
    path('', views.home, name='base'),
    path('registration/',views.registration, name='registration'),
    path('login/', views.log_in, name='log_in'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('log_out', views.log_out, name='log_out'),
    path('home/', views.view, name='home'),
    path('contact', views.contact, name='contact'),
    path('Predict/', views.predict, name='predict'),
    path('Result/', views.prediction, name='result'),
]
