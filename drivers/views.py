from django.shortcuts import render, redirect
from .models import DriverProfile
from .forms import DriverProfileForm
from django.contrib.auth.decorators import login_required
from bookings.models import Booking  # add this import
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

@login_required
def dashboard_view(request):
    try:
        profile = DriverProfile.objects.get(user=request.user)
        profile_complete = all([
            profile.contact_number,
            profile.vehicle_type,
            profile.availability,
            profile.travel_area
        ])
        # ✅ Get all bookings for this driver
        bookings = Booking.objects.filter(driver=profile)

        return render(request, 'drivers/dashboard.html', {
            'profile': profile,
            'profile_complete': profile_complete,
            'bookings': bookings  # pass to template
        })
    except DriverProfile.DoesNotExist:
        if request.method == 'POST':
            form = DriverProfileForm(request.POST, request.FILES)
            if form.is_valid():
                driver_profile = form.save(commit=False)
                driver_profile.user = request.user
                driver_profile.save()
                return redirect('drivers:dashboard')
        else:
            form = DriverProfileForm()
        return render(request, 'drivers/driver_profile_form.html', {'form': form})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import DriverProfileForm
from .models import DriverProfile

@login_required
def edit_profile_view(request):
    try:
        driver_profile = DriverProfile.objects.get(user=request.user)
    except DriverProfile.DoesNotExist:
        driver_profile = None

    if request.method == 'POST':
        form = DriverProfileForm(request.POST, request.FILES, instance=driver_profile)
        if form.is_valid():
            driver_profile = form.save(commit=False)
            driver_profile.user = request.user  # Make sure user is set
            driver_profile.save()
            return redirect('drivers:dashboard')
    else:
        form = DriverProfileForm(instance=driver_profile)

    return render(request, 'drivers/driver_profile_form.html', {'form': form})


@login_required
def accept_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.user == booking.driver.user:
        booking.status = 'Approved'
        booking.save()
        messages.success(request, "You accepted the booking.")
    return redirect('drivers:dashboard')

@login_required
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.user == booking.driver.user:
        booking.status = 'Rejected'
        booking.save()
        messages.warning(request, "You rejected the booking.")
    return redirect('drivers:dashboard')
