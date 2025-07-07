from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('technician/dashboard/', views.technician_dashboard, name='technician_dashboard'),
    path('technicians/', views.technician_list, name='technician_list'),
    path('technician/<int:technician_id>/', views.technician_profile, name='technician_profile'),
    path('book/<int:technician_id>/', views.book_technician, name='book_technician'),
    path('customer/bookings/', views.customer_bookings, name='customer_bookings'),
    path('technician/jobs/', views.technician_jobs, name='technician_jobs'),

]
