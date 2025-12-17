from datetime import datetime, time, timedelta
from typing import List

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.bookings.models import BusCompany, Route, Bus, Schedule, Seat


class Command(BaseCommand):
    help = "Seed demo data for BusCompany, Route, Bus, Schedule, and Seat."

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write(self.style.MIGRATE_HEADING("Seeding demo data..."))
            companies = self._create_companies()
            routes = self._create_routes()
            buses = self._create_buses(companies)
            schedules = self._create_schedules(routes, buses)
            self._create_seats_for_schedules(schedules)
            self.stdout.write(self.style.SUCCESS("Seeding complete."))

    # ------------------------------------------------------------------ helpers
    def _create_companies(self) -> List[BusCompany]:
        names = [
            "Tahmed",
            "Mashpoa",
            "Buscar",
            "Ena Coach",
            "Dreamline",
        ]
        companies = []
        for name in names:
            company, _ = BusCompany.objects.get_or_create(
                name=name,
                defaults={
                    "contact_email": f"info@{name.lower().replace(' ', '')}.com",
                    "contact_phone": "+254700000000",
                    "description": f"{name} bus company",
                },
            )
            companies.append(company)
        self.stdout.write(self.style.SUCCESS(f"Created/ensured {len(companies)} companies"))
        return companies

    def _create_routes(self) -> List[Route]:
        route_specs = [
            ("Nairobi", "Mombasa", 500, 510),
            ("Nairobi", "Kisumu", 350, 390),
            ("Mombasa", "Malindi", 120, 135),
            ("Nairobi", "Nakuru", 160, 150),
        ]
        routes = []
        for origin, destination, distance_km, duration_minutes in route_specs:
            route, _ = Route.objects.get_or_create(
                origin=origin,
                destination=destination,
                defaults={
                    "distance_km": distance_km,
                    "duration_minutes": duration_minutes,
                },
            )
            routes.append(route)
        self.stdout.write(self.style.SUCCESS(f"Created/ensured {len(routes)} routes"))
        return routes

    def _create_buses(self, companies: List[BusCompany]) -> List[Bus]:
        # Ten sample bus numbers in the KAB 123C format
        bus_numbers = [
            "KAB 101A",
            "KAB 202B",
            "KAB 303C",
            "KAB 404D",
            "KAB 505E",
            "KAB 606F",
            "KAB 707G",
            "KAB 808H",
            "KAB 909J",
            "KAB 010K",
        ]
        bus_types = [Bus.STANDARD, Bus.VIP, Bus.BUSINESS]
        amenities = "WiFi,AC,Charging"

        buses = []
        idx = 0
        for number in bus_numbers:
            company = companies[idx % len(companies)]
            bus, _ = Bus.objects.get_or_create(
                company=company,
                bus_number=number,
                defaults={
                    "capacity": 68 + (idx % 5),  # cycles 68–72
                    "bus_type": bus_types[idx % len(bus_types)],
                    "amenities": amenities,
                },
            )
            buses.append(bus)
            idx += 1
        self.stdout.write(self.style.SUCCESS(f"Created/ensured {len(buses)} buses"))
        return buses

    def _create_schedules(self, routes: List[Route], buses: List[Bus]) -> List[Schedule]:
        today = timezone.localdate()
        base_dates = [today, today + timedelta(days=1)]

        # Pair a few schedules: (route index, bus index, date, dep time, arr time, price)
        schedule_specs = [
            (0, 0, base_dates[0], time(7, 30), time(13, 0), 2500),
            (0, 1, base_dates[1], time(9, 0), time(14, 30), 2600),
            (1, 2, base_dates[0], time(8, 15), time(14, 0), 2200),
            (1, 3, base_dates[1], time(15, 0), time(20, 45), 2300),
            (2, 4, base_dates[0], time(10, 0), time(12, 30), 900),
            (3, 5, base_dates[1], time(6, 45), time(9, 0), 1200),
        ]

        schedules = []
        for route_idx, bus_idx, date_val, dep_t, arr_t, price in schedule_specs:
            route = routes[route_idx % len(routes)]
            bus = buses[bus_idx % len(buses)]
            departure = timezone.make_aware(datetime.combine(date_val, dep_t))
            arrival = timezone.make_aware(datetime.combine(date_val, arr_t))
            schedule, _ = Schedule.objects.get_or_create(
                route=route,
                bus=bus,
                departure_time=departure,
                defaults={
                    "arrival_time": arrival,
                    "price": price,
                    "status": Schedule.ACTIVE,
                },
            )
            schedules.append(schedule)
        self.stdout.write(self.style.SUCCESS(f"Created/ensured {len(schedules)} schedules"))
        return schedules

    def _create_seats_for_schedules(self, schedules: List[Schedule]) -> None:
        created_total = 0
        for schedule in schedules:
            # If seats already exist, skip to keep idempotency
            if schedule.seats.exists():
                continue
            capacity = schedule.bus.capacity
            seats = [
                Seat(
                    schedule=schedule,
                    seat_number=str(i + 1),
                    status=Seat.AVAILABLE,
                )
                for i in range(capacity)
            ]
            Seat.objects.bulk_create(seats)
            created_total += capacity
        self.stdout.write(self.style.SUCCESS(f"Created {created_total} seats across schedules"))

