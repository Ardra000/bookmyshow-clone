from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('<int:movie_id>/theaters/', views.theater_list, name='theater_list'),

    path('select-seats/<int:showtime_id>/', views.select_seats, name='select_seats'),
    path('booking-confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('', views.home, name='home'),
    path('theater/<int:theater_id>/seats/book/', views.book_seats, name='book_seats'),
    path('showtimes/<int:movie_id>/', views.showtimes, name='showtimes'),


]

