from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('technician', 'Technician'),
    ]

    CATEGORY_CHOICES = [
        ('ac', 'AC Repair'),
        ('electrician', 'Electrician'),
        ('laundry', 'Laundry'),
        ('carpenter', 'Carpenter'),
        ('driver', 'Driver'),
        ('plumber', 'Plumber'),
        ('pest', 'Pest Control'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_approved = models.BooleanField(default=False)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True, null=True)
    photo = models.ImageField(upload_to='technician_photos/', blank=True, null=True)
    is_available = models.BooleanField(default=True)  # 🔄 Real-time status

    def __str__(self):
        return self.username

class Booking(models.Model):
    customer = models.ForeignKey(CustomUser, related_name='customer_bookings', on_delete=models.CASCADE)
    technician = models.ForeignKey(CustomUser, related_name='technician_bookings', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default='Pending')  # Future use: 'Accepted', 'Completed'


    def __str__(self):
        return f"{self.customer.username} booked {self.technician.username}"