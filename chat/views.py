from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from bookings.models import Booking
from .models import ChatMessage


@login_required
def chat_room(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check permissions
    if request.user != booking.customer and request.user != booking.delivery_partner:
        messages.error(request, 'You do not have permission to access this chat.')
        return redirect('dashboard')
    
    # Check if chat is available (booking must be assigned)
    if booking.status not in ['assigned', 'started', 'reached', 'collected']:
        messages.error(request, 'Chat is only available for assigned bookings.')
        return redirect('dashboard')
    
    # Get existing messages
    messages_list = ChatMessage.objects.filter(booking=booking).order_by('timestamp')
    
    context = {
        'booking': booking,
        'messages': messages_list,
        'other_user': booking.delivery_partner if request.user == booking.customer else booking.customer,
    }
    
    return render(request, 'chat/chat_room.html', context)


@login_required
def get_chat_messages(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check permissions
    if request.user != booking.customer and request.user != booking.delivery_partner:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    messages_list = ChatMessage.objects.filter(booking=booking).order_by('timestamp')
    
    messages_data = [{
        'message': msg.message,
        'sender': msg.sender.mobile_number,
        'sender_type': msg.sender.user_type,
        'timestamp': msg.timestamp.isoformat(),
        'is_own': msg.sender == request.user,
    } for msg in messages_list]
    
    return JsonResponse({'messages': messages_data})
