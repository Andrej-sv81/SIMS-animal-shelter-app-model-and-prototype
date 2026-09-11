from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User

from .models import (
    Adopter,
    Animal,
    BankStatement,
    BankStatementLine,
    FosterRequest,
    Organization,
    OrganizationMembership,
)


def _load_animal_names_from_static():
    images_path = Path(settings.BASE_DIR) / "shelter" / "static" / "shelter" / "images" / "animals"
    if not images_path.exists():
        return []
    animal_names = []
    for image_file in sorted(images_path.iterdir()):
        if image_file.is_file() and image_file.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".svg"}:
            animal_names.append(image_file.stem)
    return animal_names


def initialize_seed_data():
    if Organization.objects.exists():
        return

    org = Organization.objects.create(
        name="Dječje sklonište",
        description="Organizacija podržava privremeni smještaj i udomljavanje životinja.",
    )
    admin = User.objects.create_superuser(username="orgadmin", email="admin@example.com", password="admin123")
    OrganizationMembership.objects.create(user=admin, organization=org, role=OrganizationMembership.ROLE_ADMIN)

    animal_names = _load_animal_names_from_static()
    if not animal_names:
        animal_names = [
            "Luna", "Mika", "Boki", "Nina", "Rex", "Maya", "Toby", "Kira", "Coco", "Ziko",
            "Daisy", "Kiko", "Loki", "Nora", "Panda", "Milo", "Runa", "Tara", "Yoda", "Pip",
        ]

    for name in animal_names:
        Animal.objects.create(name=name, status=Animal.STATUS_FREE, organization=org)

    adopter = Adopter.objects.create(
        first_name="Marko",
        last_name="Marković",
        phone="0912345678",
        email="marko.markovic@example.com",
        organization=org,
    )

    for animal in Animal.objects.filter(is_deleted=False)[:5]:
        FosterRequest.objects.create(
            animal=animal,
            applicant_first_name="Marko",
            applicant_last_name="Marković",
            applicant_phone="0912345678",
            applicant_email="marko.markovic@example.com",
            message="Želim pružiti ljubavnoj životinji siguran dom.",
            status=FosterRequest.STATUS_CHOICES[0][0],
        )

    BankStatement.objects.create(
        organization=org,
        uploaded_by=admin,
        account_name="Glavni račun",
        period_start="2026-01-01",
        period_end="2026-01-31",
        opening_balance=1000.00,
        closing_balance=1250.00,
    )
