"""Tests for pai end points."""
from django.test import Client
from django.test import TestCase
from django.urls import reverse
# from django.test import RequestFactory
import json


class ApiTest(TestCase):
    """Test Api View."""

    def setUp(self):
        """Set home fixture."""
        self.client = Client()

    def test_api_route_returns_status_200(self):
        """Api route returns 200."""
        play = {"board": "         ", "move": 0}
        response = self.client.post(
            reverse('bot'), json.dumps(play), content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_home_route_returns_status_200(self):
        """Api route returns 200."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
