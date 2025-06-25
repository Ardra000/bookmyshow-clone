from django.shortcuts import render

# Create your views here.
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from movies.models import Booking
from django.db.models import Sum, Count

@staff_member_required
def admin_dashboard(request):
    total_revenue = Booking.objects.aggregate(total=Sum('total_price'))['total'] or 0
    total_bookings = Booking.objects.count()

    popular_movie = (
        Booking.objects.values('movie__name')
        .annotate(count=Count('id'))
        .order_by('-count')
        .first()
    )
    popular_movie_name = popular_movie['movie__name'] if popular_movie else "No bookings yet"

    busiest_theater = (
        Booking.objects.values('theater__name')
        .annotate(count=Count('id'))
        .order_by('-count')
        .first()
    )
    busiest_theater_name = busiest_theater['theater__name'] if busiest_theater else "No bookings yet"

    context = {
        'total_revenue': total_revenue,
        'total_bookings': total_bookings,
        'popular_movie': popular_movie_name,
        'busiest_theater': busiest_theater_name,
    }
    return render(request, 'admin/custom_dashboard.html', context)