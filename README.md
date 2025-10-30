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

4. Start server:
   ```bash
   python manage.py runserver
   ```

5. Open http://127.0.0.1:8000 in browser

## Test Accounts

**Admin:**
- Mobile: 9999999999
- OTP: 1234

**Delivery Partner:**
- Mobile: 8888888888
- OTP: 1234

**Customer:**
- Mobile: 7777777777
- OTP: 1234

## Usage

1. Login with mobile number and OTP 1234
2. Customers can create bookings
3. Admins assign bookings to delivery partners
4. Delivery partners update status and chat with customers
