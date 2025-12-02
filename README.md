# TravelWave Web

A smart and modern bus booking & parcel tracking platform.

## Overview

TravelWave is a web-based transportation solution designed to simplify how passengers book buses and track parcels. Built with HTML, CSS, Bootstrap, Python, and Django, the platform allows users to book trips online, view bus schedules, track parcels, and interact with multiple bus companies in one unified ecosystem.

This project is developed as part of the incubation program at eMobilis Technology Training Institute, showcasing real-world web development practices, API integrations, and efficient system design.

## Key Features

- **Online Bus Booking** - Users can browse routes, view schedules, select bus companies, and reserve seats from anywhere.
- **Parcel Tracking Module** - Track parcel status from "Received" to "In Transit" to "Delivered".
- **Multi-Bus Company Support** - Integrates different transport companies into one platform.
- **User Authentication** - Secure login, registration, and logout using Django Auth.
- **Responsive UI** - Built with Bootstrap for a clean, mobile-friendly interface.
- **Admin Dashboard** - Bus companies can manage routes, buses, and bookings.
- **Mock Payment Integration** - API test mode or dummy payment page for demonstration.

## Tech Stack

### Frontend

- HTML
- CSS
- Bootstrap
- JavaScript

### Backend

- Python
- Django Framework

### Tools & Platforms

- Git & GitHub
- APIs (for payments and future tracking)
- Django Admin Panel

## Project Structure.

```
travelwave/
│
├── travelwave/            # Django project core
├── booking/               # Bus booking app
├── parcels/               # Parcel tracking app
├── accounts/              # User login/register
│
├── templates/             # HTML templates
├── static/                # Bootstrap, CSS, JS
│
└── README.md
```

## Setup Instructions

1. **Clone the repo:**

   ```bash
   git clone https://github.com/yourusername/travelwave-web.git
   cd travelwave-web
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server:**

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

5. **Visit the app in your browser:**

   ```
   http://127.0.0.1:8000/
   ```

## Project Tasks & Issues

All development tasks are tracked under GitHub Issues, categorized as:

- **TW-1**: Project setup
- **TW-2**: Base templates & Bootstrap
- **TW-3**: User authentication
- **TW-4**: Bus company models
- **TW-5**: Booking flow
- **TW-6**: Parcel tracking
- **TW-7**: Payment integration
- **TW-8**: UI polishing
- **TW-9**: Deployment prep

## Contributor

- **Emmanuel Kibet Kiplimo** – Solo-Developer.
