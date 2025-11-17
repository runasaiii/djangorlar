import random
from faker import Faker

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.db import transaction
from datetime import date

from apps.auths.models import CustomUser


class Command(BaseCommand):
    help = "Generate 50 demo users for ORM practice."

    def handle(self, *args, **options):
        fake = Faker()
        Faker.seed(10)
        random.seed(10)

        roles = [r[0] for r in CustomUser.ROLE_CHOICES]
        departments = ["HR", "Finance", "IT", "Sales", None, ""]

        hashed_password = make_password("12345")

        # очистить прошлых демо-пользователей (опционально)
        CustomUser.objects.filter(email__contains="demo").delete()

        users = []

        for i in range(50):

            # иногда NULL birth_date
            if random.random() < 0.15:
                birth = None
            else:
                year = random.randint(1970, 2005)
                month = random.randint(1, 12)
                day = random.randint(1, 28)
                birth = date(year, month, day)

            first = fake.first_name()
            last = fake.last_name()

            user = CustomUser(
                email=f"demo_{i}_{fake.unique.email()}",
                username=f"demo_user_{i}",
                first_name=first,
                last_name=last,
                full_name=f"{first} {last}",
                phone=fake.phone_number(),
                city=random.choice(["Almaty", "Astana", "Shymkent", "Dubai", "Paris", None, "", fake.city()]),
                country=random.choice(["Kazakhstan", "USA", "France", "Kazakhstan", "UAE"]),
                role=random.choice(roles),
                department=random.choice(departments),
                birth_date=birth,
                salary=round(random.uniform(50000, 900000), 2),
                password=hashed_password,
                is_active=random.choice([True, True, True, False]),
                is_staff=False,
                is_superuser=False,
                date_joined=timezone.now() - timezone.timedelta(days=random.randint(0, 2000)),
                last_login=None if random.random() < 0.3 else timezone.now() - timezone.timedelta(days=random.randint(0, 30)),
            )

            users.append(user)

        with transaction.atomic():
            CustomUser.objects.bulk_create(users, batch_size=50)

        self.stdout.write(self.style.SUCCESS("Successfully created 50 demo users."))
