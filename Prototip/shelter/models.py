from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.templatetags.static import static
from django.utils import timezone


class Organization(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class OrganizationMembership(models.Model):
    ROLE_ADMIN = "admin"
    ROLE_VOLUNTEER = "volunteer"
    ROLE_CHOICES = [
        (ROLE_ADMIN, "Organization Admin"),
        (ROLE_VOLUNTEER, "Volunteer"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="membership")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="members")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_VOLUNTEER)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_volunteer(self):
        return self.role == self.ROLE_VOLUNTEER


class Adopter(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="adopters")
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Animal(models.Model):
    STATUS_FREE = "Slobodna"
    STATUS_PROCESS = "U Procesu"
    STATUS_ADOPTED = "Udomljena"
    STATUS_CHOICES = [
        (STATUS_FREE, "Slobodna"),
        (STATUS_PROCESS, "U Procesu"),
        (STATUS_ADOPTED, "Udomljena"),
    ]

    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_FREE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="animals")
    adopter = models.ForeignKey(Adopter, null=True, blank=True, on_delete=models.SET_NULL, related_name="animals")
    image = models.ImageField(upload_to="shelter/images/animals/", blank=True, null=True)
    fostered_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="fostered_animals")
    fostered_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_image_url(self):
        if self.image and self.image.name:
            return self.image.url

        slug = self.name.lower().replace(" ", "-")
        images_dir = Path(settings.BASE_DIR, "shelter", "static", "shelter", "images", "animals")
        for extension in [".jpg", ".jpeg", ".png", ".webp", ".svg"]:
            candidate = images_dir / f"{slug}{extension}"
            if candidate.exists():
                return static(f"shelter/images/animals/{candidate.name}")

        if images_dir.exists():
            for candidate in images_dir.iterdir():
                if candidate.is_file() and candidate.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".svg"} and candidate.stem.lower() == slug:
                    return static(f"shelter/images/animals/{candidate.name}")

        return static("shelter/images/animals/placeholder.svg")


class FosterRequest(models.Model):
    STATUS_CHOICES = [
        ("Na čekanju", "Na čekanju"),
        ("Prihvaćen", "Prihvaćen"),
        ("Odbijen", "Odbijen"),
    ]

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="requests")
    applicant_first_name = models.CharField(max_length=100)
    applicant_last_name = models.CharField(max_length=100)
    applicant_phone = models.CharField(max_length=30)
    applicant_email = models.EmailField()
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Na čekanju")
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    adopter = models.ForeignKey(Adopter, null=True, blank=True, on_delete=models.SET_NULL, related_name="requests")
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.animal.name} - {self.status}"

    def get_description(self):
        descriptions = {
            "Luna": "Luna je mirna i društvena životinja koja dobro podnosi promjene i traži spokojan dom.",
            "Mika": "Mika je energična, znatiželjna i vrlo privržena prema ljudima.",
        }
        return descriptions.get(self.animal.name, f"{self.animal.name} je spreman za dom koji pruža ljubav i brižnost.")


class BankStatement(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="bank_statements")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    uploaded_at = models.DateTimeField(default=timezone.now)
    file = models.FileField(upload_to="bank_statements/")
    account_name = models.CharField(max_length=150, blank=True)
    period_start = models.DateField(null=True, blank=True)
    period_end = models.DateField(null=True, blank=True)
    opening_balance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    closing_balance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.organization.name} - {self.account_name or self.file.name}"


class BankStatementLine(models.Model):
    statement = models.ForeignKey(BankStatement, on_delete=models.CASCADE, related_name="lines")
    date = models.DateField()
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"{self.date} – {self.description}"
