from django.core.management.base import BaseCommand
from django.db import transaction

from apps.parcels.models import Parcel


class Command(BaseCommand):
    help = "Seed a few demo parcels for tracking."

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write(self.style.MIGRATE_HEADING("Seeding demo parcels..."))
            specs = [
                ("TW-0001-ABCD", "John Doe", "Mary Wanjiru", Parcel.STATUS_IN_TRANSIT),
                ("TW-0002-EFGH", "Acme Corp", "James Otieno", Parcel.STATUS_OUT_FOR_DELIVERY),
                ("TW-0003-IJKL", "Sarah Kim", "Peter Kariuki", Parcel.STATUS_DELIVERED),
            ]
            for tracking, sender, receiver, status in specs:
                Parcel.objects.get_or_create(
                    tracking_number=tracking,
                    defaults={
                        "sender_name": sender,
                        "receiver_name": receiver,
                        "status": status,
                    },
                )
            self.stdout.write(self.style.SUCCESS("Demo parcels seeded (or already exist)."))


