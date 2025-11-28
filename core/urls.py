from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('worker/', views.worker_dashboard, name='worker_dashboard'),
    path('worker/create-shipment/', views.create_shipment, name='create_shipment'),


]
