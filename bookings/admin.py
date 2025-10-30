from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'customer', 'delivery_partner', 'status', 
        'pickup_contact_name', 'delivery_contact_name', 
        'created_at', 'updated_at'
    )
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = (
        'customer__mobile_number', 'delivery_partner__mobile_number',
        'pickup_contact_name', 'delivery_contact_name', 'item_description'
    )
    readonly_fields = (
        'created_at', 'updated_at', 'assigned_at', 'started_at',
        'reached_at', 'collected_at', 'delivered_at', 'cancelled_at'
    )
    
    fieldsets = (
        ('Customer & Delivery Partner', {
            'fields': ('customer', 'delivery_partner', 'status')
        }),
        ('Pickup Details', {
            'fields': ('pickup_address', 'pickup_contact_name', 'pickup_contact_phone')
        }),
        ('Delivery Details', {
            'fields': ('delivery_address', 'delivery_contact_name', 'delivery_contact_phone')
        }),
        ('Item & Instructions', {
            'fields': ('item_description', 'special_instructions', 'estimated_price')
        }),
        ('Timestamps', {
            'fields': (
                'created_at', 'updated_at', 'assigned_at', 'started_at',
                'reached_at', 'collected_at', 'delivered_at', 'cancelled_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('customer', 'delivery_partner')
