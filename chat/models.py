from django.db import models
from django.conf import settings


class ChatMessage(models.Model):
    booking = models.ForeignKey(
        'bookings.Booking', 
        on_delete=models.CASCADE, 
        related_name='chat_messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"Message from {self.sender.mobile_number} for Booking #{self.booking.id}"
