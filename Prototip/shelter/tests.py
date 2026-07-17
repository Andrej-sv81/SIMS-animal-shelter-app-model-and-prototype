from django.test import TestCase
from django.urls import reverse

from .models import Animal, FosterRequest


class ShelterFlowTests(TestCase):
    def setUp(self):
        self.animal = Animal.objects.create(name="Luna", status="Slobodna", is_deleted=False)
        self.request = FosterRequest.objects.create(animal=self.animal, status="Na čekanju", is_deleted=False)

    def test_animal_list_shows_placeholder_cards(self):
        session = self.client.session
        session["is_admin_logged_in"] = True
        session.save()

        response = self.client.get(reverse("animal_list"))

        self.assertContains(response, "Luna")
        self.assertContains(response, "placeholder.svg")

    def test_seed_data_deduplicates_same_name(self):
        Animal.objects.create(name="Mika", status="Slobodna", is_deleted=False)
        Animal.objects.create(name="Mika", status="Slobodna", is_deleted=False)

        self.client.get(reverse("animal_list"))

        self.assertEqual(Animal.objects.filter(name="Mika", is_deleted=False).count(), 1)

    def test_request_detail_marks_animal_in_process(self):
        session = self.client.session
        session["is_admin_logged_in"] = True
        session.save()

        response = self.client.get(reverse("request_detail", args=[self.request.id]))

        self.assertEqual(response.status_code, 200)
        self.animal.refresh_from_db()
        self.assertEqual(self.animal.status, "U Procesu")

    def test_acceptance_marks_animal_adopted_and_deleted(self):
        session = self.client.session
        session["is_admin_logged_in"] = True
        session.save()

        response = self.client.post(reverse("close_request", args=[self.request.id]), {"decision": "prihvacen"})

        self.assertContains(response, "Zahtjev prihvaćen")
        self.animal.refresh_from_db()
        self.request.refresh_from_db()
        self.assertEqual(self.animal.status, "Udomljena")
        self.assertTrue(self.animal.is_deleted)
        self.assertTrue(self.request.is_deleted)
