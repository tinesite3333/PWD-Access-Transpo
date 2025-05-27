from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from drivers.models import DriverProfile  # ✅ Import this at the top
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Booking


@login_required
def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.pwd = request.user
            booking.save()
            return redirect('pwds:dashboard')  # adjust based on your URL name
    else:
        form = BookingForm()
    return render(request, 'bookings/create_booking.html', {'form': form})

@login_required
def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.pwd = request.user

            # ✅ Get driver ID from POST and assign it to the booking
            driver_id = request.POST.get('driver')  # assumes a hidden or select input named 'driver'
            if driver_id:
                try:
                    driver_profile = DriverProfile.objects.get(id=driver_id)
                    booking.driver = driver_profile
                except DriverProfile.DoesNotExist:
                    # Optional: handle the error or show a message
                    pass

            booking.save()
            return redirect('pwds:dashboard')  # adjust this if needed
    else:
        form = BookingForm()

    return render(request, 'bookings/create_booking.html', {'form': form})

@login_required
def accept_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.user == booking.driver.user:
        booking.status = 'Approved'
        booking.save()
        messages.success(request, "You accepted the booking.")
    return redirect('driver_dashboard')

@login_required
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.user == booking.driver.user:
        booking.status = 'Rejected'
        booking.save()
        messages.warning(request, "You rejected the booking.")
    return redirect('driver_dashboard')

def mark_arrived(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    # Check if the logged in user is the driver of the booking
    if request.user == booking.driver.user:
        booking.status = 'Completed'
        booking.save()
        messages.success(request, "You marked this trip as arrived safely.")
    else:
        messages.error(request, "You are not authorized to perform this action.")
    return redirect('drivers:dashboard')