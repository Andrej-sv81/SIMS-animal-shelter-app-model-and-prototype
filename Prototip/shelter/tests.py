from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Animal, FosterRequest, Organization, OrganizationMembership
from .seed import _load_animal_names_from_static, initialize_seed_data


class ShelterFlowTests(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(
            name="Test Shelter",
            description="Testna organizacija za udomljavanje",
        )
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="password123",
        )
        OrganizationMembership.objects.create(
            user=self.admin_user,
            organization=self.organization,
            role=OrganizationMembership.ROLE_ADMIN,
        )
        self.animal = Animal.objects.create(
            name="Luna",
            status=Animal.STATUS_FREE,
            organization=self.organization,
            is_deleted=False,
        )
        self.request = FosterRequest.objects.create(
            animal=self.animal,
            applicant_first_name="Ana",
            applicant_last_name="Anić",
            applicant_phone="0912345678",
            applicant_email="ana@example.com",
            message="Želim pružiti dom.",
            status=FosterRequest.STATUS_CHOICES[0][0],
            is_deleted=False,
        )

    def test_home_shows_organizations(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.organization.name)

    def test_organization_detail_shows_animals(self):
        response = self.client.get(reverse("organization_detail", args=[self.organization.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.animal.name)
        self.assertContains(response, "Životinje")

    def test_animal_list_shows_all_animals(self):
        response = self.client.get(reverse("animal_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.animal.name)
        self.assertContains(response, self.organization.name)

    def test_request_acceptance_creates_adopter_and_updates_status(self):
        self.client.force_login(self.admin_user)
        response = self.client.post(
            reverse("close_request", args=[self.request.id]),
            {"decision": "prihvacen"},
        )
        self.assertEqual(response.status_code, 302)

        self.request.refresh_from_db()
        self.animal.refresh_from_db()
        self.assertEqual(self.request.status, "Prihvaćen")
        self.assertEqual(self.animal.status, Animal.STATUS_ADOPTED)
        self.assertIsNotNone(self.request.adopter)
        self.assertEqual(self.animal.adopter, self.request.adopter)

    def test_request_denial_returns_animal_to_free_status(self):
        self.client.force_login(self.admin_user)
        response = self.client.post(
            reverse("close_request", args=[self.request.id]),
            {"decision": "odbijen"},
        )
        self.assertEqual(response.status_code, 302)

        self.request.refresh_from_db()
        self.animal.refresh_from_db()
        self.assertEqual(self.request.status, "Odbijen")
        self.assertEqual(self.animal.status, Animal.STATUS_FREE)

    def test_request_detail_shows_request_data(self):
        response = self.client.post(
            reverse("register_volunteer"),
            {
                "username": "volonter",
                "email": "volonter@example.com",
                "password1": "securepass123",
                "password2": "securepass123",
                "organization": self.organization.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="volonter").exists())
        self.assertTrue(
            OrganizationMembership.objects.filter(
                user__username="volonter",
                organization=self.organization,
                role=OrganizationMembership.ROLE_VOLUNTEER,
            ).exists()
        )

    def test_submit_adoption_request_creates_foster_request(self):
        response = self.client.post(
            reverse("submit_adoption_request", args=[self.animal.id]),
            {
                "first_name": "Ana",
                "last_name": "Anić",
                "phone": "0912345678",
                "email": "ana@example.com",
                "message": "Želim pružiti dom.",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            FosterRequest.objects.filter(
                animal=self.animal,
                applicant_email="ana@example.com",
                status=FosterRequest.STATUS_CHOICES[0][0],
            ).exists()
        )
        self.animal.refresh_from_db()
        self.assertEqual(self.animal.status, Animal.STATUS_PROCESS)

    def test_request_list_requires_login(self):
        response = self.client.get(reverse("request_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_login_logout_flow(self):
        login_response = self.client.post(
            reverse("login"),
            {"username": "admin", "password": "password123"},
        )
        self.assertEqual(login_response.status_code, 302)
        self.assertEqual(login_response.url, reverse("organization_list"))

        logout_response = self.client.get(reverse("logout"))
        self.assertEqual(logout_response.status_code, 302)
        self.assertEqual(logout_response.url, reverse("home"))

    def test_volunteer_can_foster_animal(self):
        volunteer_user = User.objects.create_user(
            username="volonter",
            email="volonter@example.com",
            password="volunteer123",
        )
        OrganizationMembership.objects.create(
            user=volunteer_user,
            organization=self.organization,
            role=OrganizationMembership.ROLE_VOLUNTEER,
        )
        self.client.force_login(volunteer_user)
        response = self.client.post(reverse("foster_animal", args=[self.animal.id]))
        self.assertEqual(response.status_code, 302)
        self.animal.refresh_from_db()
        self.assertEqual(self.animal.status, Animal.STATUS_PROCESS)
        self.assertEqual(self.animal.fostered_by, volunteer_user)

    def test_adopter_list_accessible_by_volunteer(self):
        volunteer_user = User.objects.create_user(
            username="volonter",
            email="volonter@example.com",
            password="volunteer123",
        )
        OrganizationMembership.objects.create(
            user=volunteer_user,
            organization=self.organization,
            role=OrganizationMembership.ROLE_VOLUNTEER,
        )
        self.client.force_login(volunteer_user)
        response = self.client.get(reverse("adopter_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Udomitelji")

    def test_add_adopter_creates_record(self):
        volunteer_user = User.objects.create_user(
            username="volonter",
            email="volonter@example.com",
            password="volunteer123",
        )
        OrganizationMembership.objects.create(
            user=volunteer_user,
            organization=self.organization,
            role=OrganizationMembership.ROLE_VOLUNTEER,
        )
        self.client.force_login(volunteer_user)
        response = self.client.post(
            reverse("add_adopter"),
            {
                "first_name": "Ivo",
                "last_name": "Ivić",
                "phone": "0915678901",
                "email": "ivo@example.com",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            self.organization.adopters.filter(
                email="ivo@example.com",
                first_name="Ivo",
                last_name="Ivić",
            ).exists()
        )

    def test_request_detail_shows_request_data(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse("request_detail", args=[self.request.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ana")
        self.assertContains(response, "Anić")
        self.assertContains(response, "0912345678")
        self.assertContains(response, "ana@example.com")
        self.assertContains(response, "Želim pružiti dom.")

    def test_organization_animals_listed_on_detail(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse("organization_detail", args=[self.organization.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.animal.name)
        self.assertContains(response, "Životinje")

    def test_delete_organization_marks_inactive(self):
        self.client.force_login(self.admin_user)
        response = self.client.post(reverse("delete_organization", args=[self.organization.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Organization.objects.filter(id=self.organization.id, is_active=True).exists())

    def test_organization_volunteers_displays_registered_volunteer(self):
        volunteer_user = User.objects.create_user(
            username="volonter",
            email="volonter@example.com",
            password="volunteer123",
        )
        OrganizationMembership.objects.create(
            user=volunteer_user,
            organization=self.organization,
            role=OrganizationMembership.ROLE_VOLUNTEER,
        )
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse("organization_volunteers", args=[self.organization.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "volonter")
        self.assertContains(response, "Volunteer")

    def test_initialize_seed_data_loads_animals_from_static_images(self):
        Organization.objects.all().delete()
        User.objects.filter(username="orgadmin").delete()

        initialize_seed_data()
        image_names = _load_animal_names_from_static()

        self.assertGreater(len(image_names), 0)
        self.assertEqual(Animal.objects.filter(organization__name="Dječje sklonište").count(), len(image_names))
        for expected_name in image_names:
            self.assertTrue(Animal.objects.filter(name=expected_name).exists())
