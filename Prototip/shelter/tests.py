from django.test import TestCase
from django.urls import reverse

from .models import Animal, FosterRequest
from .views import ensure_seed_data


class ShelterFlowTests(TestCase):
    def setUp(self):
        self.animal = Animal.objects.create(name="Luna", status="Slobodna", is_deleted=False)
        self.request = FosterRequest.objects.create(animal=self.animal, status="Na čekanju", is_deleted=False)

    def test_animal_list_shows_cards(self):
        session = self.client.session
        session["is_admin_logged_in"] = True
        session.save()

        response = self.client.get(reverse("animal_list"))

        self.assertContains(response, "Luna")
        self.assertContains(response, "<img")

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

    def test_reset_seed_data_recreates_initial_state(self):
        Animal.objects.create(name="Custom", status="Udomljena", is_deleted=False)
        FosterRequest.objects.create(animal=self.animal, status="Prihvaćen", is_deleted=False)

        ensure_seed_data(force_reset=True)

        self.assertEqual(Animal.objects.filter(is_deleted=False).count(), 20)
        self.assertEqual(FosterRequest.objects.filter(is_deleted=False).count(), 10)

    def test_request_detail_shows_unique_description(self):
        session = self.client.session
        session["is_admin_logged_in"] = True
        session.save()

        response = self.client.get(reverse("request_detail", args=[self.request.id]))

        self.assertContains(response, self.request.get_description())

    def test_acceptance_marks_animal_adopted_and_keeps_it_visible(self):
        session = self.client.session
        session["is_admin_logged_in"] = True
        session.save()

        response = self.client.post(reverse("close_request", args=[self.request.id]), {"decision": "prihvacen"})

        self.assertContains(response, "Zahtjev prihvaćen")
        self.animal.refresh_from_db()
        self.request.refresh_from_db()
        self.assertEqual(self.animal.status, "Udomljena")
        self.assertFalse(self.animal.is_deleted)
        self.assertEqual(self.request.status, "Prihvaćen")

        adopted_response = self.client.get(reverse("adopted_animals_list"))
        self.assertContains(adopted_response, "Luna")

    def test_returning_animal_moves_it_back_to_active_list(self):
        session = self.client.session
        session["is_admin_logged_in"] = True
        session.save()

        self.animal.status = "Udomljena"
        self.animal.is_deleted = False
        self.animal.save(update_fields=["status", "is_deleted"])

        response = self.client.post(reverse("return_animal", args=[self.animal.id]))

        self.assertContains(response, "Životinja vraćena")
        self.animal.refresh_from_db()
        self.assertEqual(self.animal.status, "Slobodna")
        self.assertFalse(self.animal.is_deleted)

        active_response = self.client.get(reverse("animal_list"))
        self.assertContains(active_response, "Luna")

        adopted_response = self.client.get(reverse("adopted_animals_list"))
        self.assertNotContains(adopted_response, "Luna")
