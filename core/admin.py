from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Booking

# Register CustomUser with extended UserAdmin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_approved', 'is_staff')
    list_filter = ('role', 'is_approved', 'is_staff')
    list_editable = ('is_approved',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'is_approved', 'category', 'photo', 'is_available')}),
    )

# Register Booking model
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'technician', 'timestamp', 'status')
    list_filter = ('status', 'timestamp')
    list_editable = ('status',)
