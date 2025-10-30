from django.contrib import admin
from .models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('booking', 'sender', 'message', 'timestamp', 'is_read')
    list_filter = ('timestamp', 'is_read')
    search_fields = ('booking__id', 'sender__mobile_number', 'message')
    readonly_fields = ('timestamp',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('booking', 'sender')
