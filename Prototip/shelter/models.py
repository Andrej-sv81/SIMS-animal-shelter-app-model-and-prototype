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

    def get_description(self):
        descriptions = {
            "Luna": "Luna je mirna i društvena životinja koja dobro podnosi promjene i traži spokojan dom.",
            "Mika": "Mika je energična, znatiželjna i vrlo privržena prema ljudima.",
            "Boki": "Boki je nježan i pažljiv ljubimac koji voli tišinu i blizinu.",
            "Nina": "Nina je svestrana i vrlo prilagodljiva, idealna za obitelj s djecom.",
            "Rex": "Rex je hrabar i odan, spreman za aktivan život uz novu obitelj.",
            "Maya": "Maya je nježna i inteligentna životinja koja brzo uspostavlja kontakt.",
            "Toby": "Toby je razigran i društven, voli igru i pažnju.",
            "Kira": "Kira je tiha i suosjećajna, traži stabilan i toplu dom.",
            "Coco": "Coco je pozitivna i vesela životinja koja donosi energiju u dom.",
            "Ziko": "Ziko je znatiželjan i aktivan, voli istraživanje i kratke šetnje.",
            "Daisy": "Daisy je nježna i mirna, savršena za miran dom.",
            "Kiko": "Kiko je vrlo druželjubiv i brzo se prilagođava novim okolnostima.",
            "Loki": "Loki je sretan i komunikativan, voli blizinu ljudi.",
            "Nora": "Nora je inteligentna i poslušna, spremna za spokojan život u obitelji.",
            "Panda": "Panda je mekana i smirena, idealna za tihe domove.",
            "Milo": "Milo je srdačan i aktivan, traži dom s vremena za igru.",
            "Runa": "Runa je nježna i prilagodljiva, voli svakodnevnu rutinu.",
            "Tara": "Tara je druželjubiva i osjećajna, vrlo prikladna za ljubitelje životinja.",
            "Yoda": "Yoda je miran i promišljen, traži mirno i sigurno okruženje.",
            "Pip": "Pip je mali, živahni i vrlo drage naravi, spreman za ljubav.",
        }
        return descriptions.get(self.animal.name, f"{self.animal.name} je spreman za dom koji pruža ljubav i brižnost.")
