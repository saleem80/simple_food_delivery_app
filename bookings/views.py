from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Booking
from .forms import BookingForm
from accounts.models import User
import json


@login_required
def create_booking(request):
    if request.user.user_type != 'customer':
        messages.error(request, 'Only customers can create bookings.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.save()
            messages.success(request, 'Booking created successfully!')
            return redirect('dashboard')
    else:
        form = BookingForm()
    
    return render(request, 'bookings/create_booking.html', {'form': form})


@login_required
def view_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check permissions
    if request.user.user_type == 'customer' and booking.customer != request.user:
        messages.error(request, 'You can only view your own bookings.')
        return redirect('dashboard')
    elif request.user.user_type == 'delivery_partner' and booking.delivery_partner != request.user:
        messages.error(request, 'You can only view your assigned bookings.')
        return redirect('dashboard')
    
    return render(request, 'bookings/view_booking.html', {'booking': booking})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.user.user_type != 'customer' or booking.customer != request.user:
        messages.error(request, 'You can only cancel your own bookings.')
        return redirect('dashboard')
    
    if not booking.can_be_cancelled():
        messages.error(request, 'This booking cannot be cancelled.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        booking.update_status('cancelled')
        messages.success(request, 'Booking cancelled successfully!')
        return redirect('dashboard')
    
    return render(request, 'bookings/cancel_booking.html', {'booking': booking})


@login_required
@csrf_exempt
def assign_booking(request):
    if request.user.user_type != 'admin':
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        booking_id = data.get('booking_id')
        delivery_partner_id = data.get('delivery_partner_id')
        
        try:
            booking = Booking.objects.get(id=booking_id)
            delivery_partner = User.objects.get(id=delivery_partner_id, user_type='delivery_partner')
            
            booking.delivery_partner = delivery_partner
            booking.update_status('assigned')
            
            return JsonResponse({'success': True})
        except (Booking.DoesNotExist, User.DoesNotExist):
            return JsonResponse({'error': 'Invalid booking or delivery partner'}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
@csrf_exempt
def update_booking_status(request):
    if request.user.user_type != 'delivery_partner':
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        booking_id = data.get('booking_id')
        new_status = data.get('status')
        
        try:
            booking = Booking.objects.get(id=booking_id, delivery_partner=request.user)
            
            # Validate status progression
            valid_statuses = ['started', 'reached', 'collected', 'delivered']
            if new_status not in valid_statuses:
                return JsonResponse({'error': 'Invalid status'}, status=400)
            
            booking.update_status(new_status)
            
            return JsonResponse({
                'success': True,
                'status': booking.get_status_display()
            })
        except Booking.DoesNotExist:
            return JsonResponse({'error': 'Booking not found'}, status=404)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
