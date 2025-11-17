#Python modules
import random
from faker import Faker

#Django modules
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from datetime import date
from django.utils import timezone
from django.db import transaction

#Python modules
from apps.auths.models import CustomUser


class Command(BaseCommand):
    help = "Generate 10k users for testing in bulk."

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10000,
            help='Number of users to generate'
        )
        parser.add_argument(
            '--batch',
            type=int,
            default=1000,
            help='Number of users to create in each batch'
        )

    def handle(self, *args, **options):
        count = options['count']
        batch = options['batch']
        fake = Faker()
        Faker.seed(0)
        random.seed(0)

        roles =  [CustomUser.ROLE_CHOICES[i][0] for i in range(len(CustomUser.ROLE_CHOICES))]
        departments = [
            'HR',
            'Finance',
            'IT',
            'Sales'
        ]

        hashed_password = make_password("12345")
        users_to_create = []
        created = 0

        fake_unique = Faker()
        fake_unique.seed_instance(1)
        fake_unique.unique.clear()

        for _ in range(count):
            year = random.randint(1975, 2005)
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            birth = date(year, month, day)
            
            email = fake_unique.unique.email()
            username = fake_unique.unique.user_name()
            first_name = fake.first_name()
            last_name = fake.last_name()
            full_name = f"{first_name} {last_name}"
            phone = fake.phone_number()
            city = fake.city()
            country = fake.country()
            role = random.choice(roles)
            department = random.choice(departments)
            salary = round(random.uniform(10000, 100000), 2)

            user = CustomUser(
                email=email,
                username=username,
                full_name=full_name,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                city=city,
                country=country,
                role=role,
                department=department,
                birth_date=birth,
                salary=salary,
                password=hashed_password,
                is_active=True,
                is_staff=(role == CustomUser.ROLE_CHOICES[2][0]),
                is_superuser=(role == CustomUser.ROLE_CHOICES[2][0]),
                date_joined=timezone.now().date(),
                last_login=None,
            )
            users_to_create.append(user)

            if len(users_to_create) >= batch:
                with transaction.atomic():
                    CustomUser.objects.bulk_create(users_to_create, batch_size=batch)
                created += len(users_to_create)
                self.stdout.write(self.style.SUCCESS(f'Created {created}/{count} users...'))
                users_to_create = []

        if users_to_create:
            with transaction.atomic():
                CustomUser.objects.bulk_create(users_to_create, batch_size=batch)
            created += len(users_to_create)
            self.stdout.write(self.style.SUCCESS(f'Created {created}/{count} users...'))

        self.stdout.write(self.style.SUCCESS(f'Successfully created 10k users.'))