from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='accounts_dashboard'),
]