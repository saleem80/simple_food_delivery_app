from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, OTPVerification


class UserAdmin(BaseUserAdmin):
    list_display = ('mobile_number', 'first_name', 'last_name', 'user_type', 'is_active', 'is_staff')
    list_filter = ('user_type', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('mobile_number', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Delivery Partner', {'fields': ('is_available',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile_number', 'first_name', 'last_name', 'user_type', 'password1', 'password2'),
        }),
    )
    search_fields = ('mobile_number', 'first_name', 'last_name')
    ordering = ('mobile_number',)


@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ('mobile_number', 'otp', 'created_at', 'is_verified')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('mobile_number',)
    readonly_fields = ('created_at',)


admin.site.register(User, UserAdmin)
