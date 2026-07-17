from pathlib import Path

from django.conf import settings
from django.db import models
from django.templatetags.static import static


class Animal(models.Model):
    STATUS_CHOICES = [
        ("Slobodna", "Slobodna"),
        ("U Procesu", "U Procesu"),
        ("Udomljena", "Udomljena"),
    ]

    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Slobodna")
    image = models.ImageField(upload_to="shelter/images/animals/", blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_image_url(self):
        if self.image and self.image.name:
            return self.image.url

        slug = self.name.lower().replace(" ", "-")
        for extension in [".jpg", ".jpeg", ".png", ".webp", ".svg"]:
            candidate = Path(settings.BASE_DIR, "shelter", "static", "shelter", "images", "animals", f"{slug}{extension}")
            if candidate.exists():
                return static(f"shelter/images/animals/{slug}{extension}")

        return static("shelter/images/animals/placeholder.svg")


class FosterRequest(models.Model):
    STATUS_CHOICES = [
        ("Na čekanju", "Na čekanju"),
        ("Prihvaćen", "Prihvaćen"),
        ("Odbijen", "Odbijen"),
    ]

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="requests")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Na čekanju")
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.animal.name} - {self.status}"
