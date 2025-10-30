from accounts.models import User
from bookings.models import Booking

# Create admin user
admin_user, created = User.objects.get_or_create(
    mobile_number='9999999999',
    defaults={
        'user_type': 'admin',
        'first_name': 'Admin',
        'last_name': 'User',
        'is_staff': True,
        'is_superuser': True
    }
)
if created:
    print("Created admin user: 9999999999")

# Create delivery partners
delivery_partners_data = [
    {'mobile': '8888888888', 'first_name': 'John', 'last_name': 'Doe'},
    {'mobile': '7777777777', 'first_name': 'Jane', 'last_name': 'Smith'},
    {'mobile': '6666666666', 'first_name': 'Mike', 'last_name': 'Johnson'},
]

for partner_data in delivery_partners_data:
    partner, created = User.objects.get_or_create(
        mobile_number=partner_data['mobile'],
        defaults={
            'user_type': 'delivery_partner',
            'first_name': partner_data['first_name'],
            'last_name': partner_data['last_name']
        }
    )
    if created:
        print(f"Created delivery partner: {partner_data['mobile']}")

# Create sample customer
customer, created = User.objects.get_or_create(
    mobile_number='5555555555',
    defaults={
        'user_type': 'customer',
        'first_name': 'Test',
        'last_name': 'Customer'
    }
)
if created:
    print("Created sample customer: 5555555555")

# Create sample booking
booking, created = Booking.objects.get_or_create(
    customer=customer,
    defaults={
        'pickup_address': '123 Restaurant Street, Downtown, City 12345',
        'pickup_contact_name': 'Restaurant Manager',
        'pickup_contact_phone': '1234567890',
        'delivery_address': '456 Customer Avenue, Suburb, City 54321',
        'delivery_contact_name': 'Test Customer',
        'delivery_contact_phone': '5555555555',
        'item_description': 'Pizza Margherita (Large), Coca Cola (2L), Garlic Bread',
        'special_instructions': 'Please ring the doorbell twice. Leave at door if no answer.',
        'estimated_price': 25.99
    }
)
if created:
    print(f"Created sample booking: #{booking.id}")

print("\nSample data created successfully!")
print("\nTest Accounts:")
print("Admin: 9999999999 (OTP: 1234)")
print("Delivery Partners: 8888888888, 7777777777, 6666666666 (OTP: 1234)")
print("Customer: 5555555555 (OTP: 1234)")
print("\nNote: Any mobile number can be used for customer registration.")