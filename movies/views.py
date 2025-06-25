from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Theater, Seat, Booking, Showtime
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum
from django.db.models import F



def homepage(request):
    today = now().date()
    today_shows = Showtime.objects.filter(start_time__date=today)
    context = {'today_shows': today_shows}
    return render(request, 'movies/home.html', context)

def home(request):
    today = now().date()
    today_shows = Showtime.objects.filter(start_time__date=today)
    return render(request, 'movies/home.html', {'today_shows': today_shows})


def movie_list(request):
    search_query = request.GET.get('search')
    if search_query:
        movies = Movie.objects.filter(name__icontains=search_query)
    else:
        movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})

def theater_list(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    theater = Theater.objects.filter(movie=movie)
    return render(request, 'movies/theater_list.html', {'movie': movie, 'theaters': theater})

def showtimes(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    showtimes = Showtime.objects.filter(movie=movie).order_by('start_time')
    return render(request, 'movies/showtimes.html', {'movie': movie, 'showtimes': showtimes})

def select_seats(request, showtime_id):
    showtime = get_object_or_404(Showtime, id=showtime_id)
    seats = Seat.objects.filter(theater=showtime.theater)

    context = {
        'theaters': showtime,
        'seats': seats,
    }
    return render(request, 'movies/select_seats.html', context)

def seat_selection(request):
    return render(request, 'movies/seat_selection.html')

@login_required(login_url='/login/')
def book_seats(request, theater_id):
    theater = get_object_or_404(Theater, id=theater_id)
    seats = Seat.objects.filter(theater=theater)

    if request.method == 'POST':
        selected_seats = request.POST.getlist('seats')
        error_seats = []

        if not selected_seats:
            return render(request, "movies/select_seats.html", {
                'theater': theater,
                'seats': seats,
                'error': "No seat selected"
            })

        for seat_id in selected_seats:
            seat = get_object_or_404(Seat, id=seat_id, theater=theater)
            if seat.is_booked:
                error_seats.append(seat.seat_number)
                continue

            try:
                Booking.objects.create(
                    user=request.user,
                    seat=seat,
                    movie=theater.movie,
                    theater=theater
                )
                seat.is_booked = True
                seat.save()
            except IntegrityError:
                error_seats.append(seat.seat_number)

        if error_seats:
            error_message = f"The following seats are already booked: {', '.join(error_seats)}"
            return render(request, 'movies/select_seats.html', {
                'theater': theater,
                'seats': seats,
                'error': error_message
            })

        return redirect('profile')

    return render(request, 'movies/select_seats.html', {
        'theater': theater,
        'seats': seats
    })

def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'movies/booking_confirmation.html', {'booking': booking})
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    total_revenue = Booking.objects.aggregate(total=Sum('total_price'))['total'] or 0
    total_bookings = Booking.objects.count()

    popular_movie = (
        Movie.objects.annotate(bookings=Count('booking'))
        .order_by('-bookings')
        .first()
    )

    busiest_theater = (
        Theater.objects.annotate(bookings=Count('show__booking'))
        .order_by('-bookings')
        .first()
    )

    context = {
        'total_revenue': total_revenue,
        'total_bookings': total_bookings,
        'popular_movie': popular_movie,
        'busiest_theater': busiest_theater,
    }

    return render(request, 'admin_dashboard.html', context)

def admin_dashboard(request):
    # Total revenue
    total_revenue = Booking.objects.aggregate(total=Sum('total_price'))['total'] or 0

    # Top 5 most popular movies by number of bookings
    popular_movies = (
        Booking.objects.values('show__movie__name')
        .annotate(bookings=Count('id'))
        .order_by('-bookings')[:5]
    )

    # Top 5 busiest theaters by number of bookings
    busiest_theaters = (
        Booking.objects.values('show__theater__name', 'show__movie__name')
        .annotate(bookings=Count('id'))
        .order_by('-bookings')[:5]
    )

    context = {
        'total_revenue': total_revenue,
        'popular_movies': popular_movies,
        'busiest_theaters': busiest_theaters,
    }
    return render(request, 'admin_dashboard.html', context)