from django.db import models
from django.conf import settings
from django.utils import timezone


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('started', 'Started'),
        ('reached', 'Reached'),
        ('collected', 'Collected'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='customer_bookings'
    )
    delivery_partner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='delivery_bookings'
    )
    
    # Pickup details
    pickup_address = models.TextField()
    pickup_contact_name = models.CharField(max_length=100)
    pickup_contact_phone = models.CharField(max_length=15)
    
    # Delivery details
    delivery_address = models.TextField()
    delivery_contact_name = models.CharField(max_length=100)
    delivery_contact_phone = models.CharField(max_length=15)
    
    # Booking details
    item_description = models.TextField()
    special_instructions = models.TextField(blank=True)
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Status and timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Status timestamp tracking
    assigned_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    reached_at = models.DateTimeField(null=True, blank=True)
    collected_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Booking #{self.id} - {self.customer.mobile_number} ({self.status})"
    
    def can_be_cancelled(self):
        return self.status in ['pending', 'assigned']
    
    def update_status(self, new_status):
        self.status = new_status
        timestamp_field = f"{new_status}_at"
        
        if hasattr(self, timestamp_field):
            setattr(self, timestamp_field, timezone.now())
        
        self.save()
