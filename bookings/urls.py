from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_booking, name='create_booking'),
    path('<int:booking_id>/', views.view_booking, name='view_booking'),
    path('<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('assign/', views.assign_booking, name='assign_booking'),
    path('update-status/', views.update_booking_status, name='update_booking_status'),
]