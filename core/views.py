from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserCreationForm
from .models import CustomUser, Booking


def home(request):
    return render(request, 'core/home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            if user.role == 'technician' and not user.is_approved:
                messages.error(request, "Your account is not approved yet.")
                return redirect('login')

            login(request, user)

            if user.role == 'customer':
                return redirect('customer_dashboard')
            elif user.role == 'technician':
                return redirect('technician_dashboard')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'core/login.html')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            if user.role == 'technician':
                user.is_approved = False  # Requires admin approval
            user.save()
            messages.success(request, "Account created successfully. Please login.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'core/register.html', {'form': form})


@login_required
def customer_dashboard(request):
    return render(request, 'core/customer_dashboard.html')


@login_required
def technician_dashboard(request):
    bookings = Booking.objects.filter(technician=request.user).order_by('-timestamp')
    return render(request, 'core/technician_dashboard.html', {'bookings': bookings})


@login_required
def customer_bookings(request):
    bookings = Booking.objects.filter(customer=request.user)
    return render(request, 'core/customer_bookings.html', {'bookings': bookings})


@login_required
def technician_jobs(request):
    bookings = Booking.objects.filter(technician=request.user)
    return render(request, 'core/technician_jobs.html', {'bookings': bookings})


@login_required
def technician_list(request):
    category = request.GET.get('category')
    technicians = CustomUser.objects.filter(role='technician', is_approved=True)
    if category:
        technicians = technicians.filter(category=category)
    return render(request, 'core/technician_list.html', {
        'technicians': technicians,
        'selected_category': category,
    })


@login_required
def technician_profile(request, technician_id):
    technician = get_object_or_404(CustomUser, id=technician_id, role='technician', is_approved=True)
    return render(request, 'core/technician_profile.html', {'technician': technician})


@login_required
def book_technician(request, technician_id):
    technician = get_object_or_404(CustomUser, id=technician_id, role='technician')
    Booking.objects.create(customer=request.user, technician=technician)

    # ✅ Send booking confirmation email
    send_mail(
        subject="Booking Confirmed",
        message=f"You booked {technician.username} for {technician.category}.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[request.user.email],
        fail_silently=True,
    )

    messages.success(request, f"You booked {technician.username} successfully!")
    return redirect('technician_list')  # ✅ FIXED: match name in urls.py
