from django.db import models
from django.contrib.auth.models import User 


# In models.py

class Movie(models.Model):
    name = models.CharField(max_length=255)
    rating = models.CharField(max_length=10, default='Not Rated')
    cast = models.TextField(blank=True, null=True)
    
    # ✅ This line should be added below other fields:
    image = models.ImageField(upload_to='movies/', null=True, blank=True)

    def __str__(self):
        return self.name
class Theater(models.Model):
    name = models.CharField(max_length=255)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

class Seat(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)

class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    show_date = models.DateField()
    show_time = models.TimeField()
    start_time = models.DateTimeField()  # used for filtering today


class Booking(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="booking")
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name="booking")
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    booking_time = models.DateTimeField(auto_now_add=True)
    related_name="booking"
    
class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    show_time = models.DateTimeField()
