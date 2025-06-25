# movies/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import Movie, Theater, Seat, Booking, Showtime

# Add this method to show image preview in admin
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image_tag')  # Show image preview
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="150" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image Preview'

class TheaterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'movie', 'theater')

# ✅ Register models
admin.site.register(Movie, MovieAdmin)
admin.site.register(Theater, TheaterAdmin)
admin.site.register(Seat)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Showtime)
