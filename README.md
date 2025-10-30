# Food Delivery App

A simple food delivery web app built with Django.

## Features
- Mobile OTP authentication (OTP: 1234)
- Role-based access (Customer, Delivery Partner, Admin)
- Booking management
- Real-time chat between customers and delivery partners
- Responsive web interface

## Quick Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```bash
   python manage.py migrate
   ```

3. Create sample data:
   ```bash
   python manage.py shell < create_sample_data.py
   ```

4. Start servers (both for full functionality):

   **For WebSocket/Chat support (Daphne):**
   ```bash
   python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery.settings'); import django; django.setup(); from daphne.cli import CommandLineInterface; CommandLineInterface().run(['food_delivery.asgi:application', '--port', '8000'])"
   ```

   **For regular development (Django dev server):**
   ```bash
   python manage.py runserver 8001
   ```

   Or run both simultaneously for full functionality!

5. Open browsers:
   - **Chat/WebSocket features:** http://127.0.0.1:8000
   - **Regular features:** http://127.0.0.1:8001

## Test Accounts

**Admin:**
- Mobile: 9999999999
- OTP: 1234

**Delivery Partners:**
- Mobile: 8888888888 (John Doe)
- Mobile: 7777777777 (Jane Smith)
- Mobile: 6666666666 (Mike Johnson)

**Customer:**
- Mobile: 5555555555
- OTP: 1234

## Usage

1. Login with mobile number and OTP 1234
2. Customers can create bookings
3. Admins assign bookings to delivery partners
4. Delivery partners update status and chat with customers
