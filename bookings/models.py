from django.db import models
from django.conf import settings
from drivers.models import DriverProfile
from datetime import date, time
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

def default_travel_time():
    return time(8, 0)

class Booking(models.Model):
    pwd = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    driver = models.ForeignKey(DriverProfile, on_delete=models.CASCADE, related_name='bookings')
    destination = models.CharField(max_length=255)
    pickup_location = models.CharField(max_length=255)
    travel_date = models.DateField(default=date.today)
    travel_time = models.TimeField(null=True, blank=True, default=default_travel_time)
    status = models.CharField(
        max_length=50,
        choices=[
            ('Pending', 'Pending'),
            ('Approved', 'Approved'),
            ('Rejected', 'Rejected'),
            ('Completed', 'Completed')
        ],
        default='Pending'
    )

    def __str__(self):
        return f"{self.pwd.username} → {self.driver.user.username} on {self.travel_date}"
    
    
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
