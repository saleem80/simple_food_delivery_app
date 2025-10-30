from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from .models import User, OTPVerification
from .forms import LoginForm, OTPForm, RegistrationForm
import json


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            mobile_number = form.cleaned_data['mobile_number']
            user_type = form.cleaned_data['user_type']
            
            # Check if user exists
            try:
                user = User.objects.get(mobile_number=mobile_number, user_type=user_type)
            except User.DoesNotExist:
                if user_type == 'customer':
                    # Check if user exists with different user_type
                    existing_user = User.objects.filter(mobile_number=mobile_number).first()
                    if existing_user:
                        messages.error(request, f'This mobile number is allready registered.')
                        return render(request, 'accounts/login.html', {'form': form})
                    
                    # Create new customer account
                    user = User.objects.create_user(
                        mobile_number=mobile_number,
                        user_type='customer'
                    )
                else:
                    messages.error(request, 'User not found. Please contact admin.')
                    return render(request, 'accounts/login.html', {'form': form})
            
            # Generate and save OTP (static OTP: 1234)
            otp_obj, created = OTPVerification.objects.get_or_create(
                mobile_number=mobile_number,
                defaults={'otp': '1234'}
            )
            if not created:
                otp_obj.otp = '1234'
                otp_obj.created_at = timezone.now()
                otp_obj.is_verified = False
                otp_obj.save()
            
            request.session['mobile_number'] = mobile_number
            request.session['user_type'] = user_type
            messages.success(request, f'OTP sent to {mobile_number}. Use: 1234')
            return redirect('verify_otp')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def verify_otp_view(request):
    mobile_number = request.session.get('mobile_number')
    user_type = request.session.get('user_type')
    
    if not mobile_number:
        return redirect('login')
    
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            
            try:
                otp_obj = OTPVerification.objects.get(
                    mobile_number=mobile_number,
                    otp=otp,
                    is_verified=False
                )
                
                if otp_obj.is_expired():
                    messages.error(request, 'OTP has expired. Please try again.')
                    return redirect('login')
                
                # Verify OTP
                otp_obj.is_verified = True
                otp_obj.save()
                
                # Login user
                user = User.objects.get(mobile_number=mobile_number, user_type=user_type)
                login(request, user)
                
                # Clear session
                del request.session['mobile_number']
                del request.session['user_type']
                
                messages.success(request, 'Login successful!')
                return redirect('dashboard')
                
            except OTPVerification.DoesNotExist:
                messages.error(request, 'Invalid OTP. Please try again.')
    else:
        form = OTPForm()
    
    return render(request, 'accounts/verify_otp.html', {
        'form': form, 
        'mobile_number': mobile_number
    })


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')


def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    context = {
        'user': request.user,
    }
    
    if request.user.user_type == 'customer':
        from bookings.models import Booking
        context['bookings'] = Booking.objects.filter(customer=request.user)
        return render(request, 'accounts/customer_dashboard.html', context)
    
    elif request.user.user_type == 'delivery_partner':
        from bookings.models import Booking
        context['bookings'] = Booking.objects.filter(delivery_partner=request.user)
        return render(request, 'accounts/delivery_dashboard.html', context)
    
    elif request.user.user_type == 'admin':
        from bookings.models import Booking
        context['all_bookings'] = Booking.objects.all()
        context['delivery_partners'] = User.objects.filter(user_type='delivery_partner')
        return render(request, 'accounts/admin_dashboard.html', context)
    
    return render(request, 'accounts/dashboard.html', context)
