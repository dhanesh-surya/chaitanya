from django.test import TestCase
from django.urls import reverse
from .models import Happening

class HappeningsTests(TestCase):
    def setUp(self):
        # Create some test happenings
        Happening.objects.create(
            title="Career Guidance Seminar 2026",
            category="Career Counselling",
            image_url="https://example.com/image1.jpg",
            link="/event-details/148/index.html"
        )
        Happening.objects.create(
            title="NSS Annual Camp",
            category="NSS",
            image_url="https://example.com/image2.jpg",
            link="/event-details/145/index.html"
        )

    def test_home_page_contains_happenings(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('happenings', response.context)
        self.assertEqual(len(response.context['happenings']), 2)

    def test_happenings_page_lists_all(self):
        response = self.client.get(reverse('core:happenings'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('page_obj', response.context)
        # Check that both test happenings are listed
        self.assertEqual(len(response.context['page_obj']), 2)
        self.assertContains(response, "Career Guidance Seminar 2026")
        self.assertContains(response, "NSS Annual Camp")

    def test_happenings_search(self):
        # Search for NSS
        response = self.client.get(reverse('core:happenings') + "?q=NSS")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 1)
        self.assertContains(response, "NSS Annual Camp")
        self.assertNotContains(response, "Career Guidance Seminar 2026")

        # Search for Career
        response = self.client.get(reverse('core:happenings') + "?q=Career")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 1)
        self.assertContains(response, "Career Guidance Seminar 2026")
        self.assertNotContains(response, "NSS Annual Camp")

        # Search for non-existent
        response = self.client.get(reverse('core:happenings') + "?q=NonExistent")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 0)
        self.assertContains(response, "No happenings found matching your filters.")

    def test_happening_detail_view_success(self):
        h = Happening.objects.create(
            title="Test Event Detail Page",
            description="<p>This is a test description.</p>",
            participants_count=150,
            registration_link="https://docs.google.com/forms/d/testform"
        )
        response = self.client.get(reverse('core:happening_detail', args=[h.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Event Detail Page")
        self.assertContains(response, "This is a test description.")
        self.assertContains(response, "150")
        self.assertContains(response, "https://docs.google.com/forms/d/testform")


class AdminTests(TestCase):
    def test_admin_login_page_loads(self):
        response = self.client.get(reverse('admin:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django administration")
