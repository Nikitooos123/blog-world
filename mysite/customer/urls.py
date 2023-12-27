from django.urls import path, include

from . import views

app_name = 'customer'

urlpatterns = [
    # url-адреса регистрации
    path('register/', views.register, name='register'),
    path('', include('django.contrib.auth.urls')),
    path('', views.news, name='news'),
    path('edit/', views.edit, name='edit'),
    path('subscription/', views.subscription, name='subscription'),
]

