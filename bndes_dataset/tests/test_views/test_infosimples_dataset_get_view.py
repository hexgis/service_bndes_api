from unittest import mock

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from bndes_dataset.tests import recipes
from bndes_dataset import models


class TestBNDESDatasetGetView(TestCase):
    """Test case for UserSettings views."""

    def setUp(self):
        """Set up data for tests, created BNDES tag and url."""

        self.recipes = recipes.BNDESDatasetRecipes()
        self.tag = self.recipes.tag.make()
        self.url = self.recipes.url.make(tags=[self.tag])

        self.mock_data_json = {"cpf": "00000000000"}

        self.assertEqual(models.BNDESTag.objects.count(), 1)
        self.assertEqual(models.BNDESUrl.objects.count(), 1)

    def get_client(self, token: str = None):
        """Test method to request data from API using APIClient.

        Arguments:
            token (Token, optional): User Token for client.
                Defaults to None.

        Returns:
            client (APIClient): APIClient from drf test.
        """
        if not token:
            token = ''

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        return client

    def test_view_exists(self):
        """Test if reverse for url asserts on real url."""
        self.assertTrue(reverse('bndes_dataset:search'))

    def test_bndes_dataset_get_view(self):
        """Test BNDESDataset view with correct data."""

        client = self.get_client()
        url_creation = reverse('bndes_dataset:search')

        request = client.post(
            url_creation, self.mock_data_json, format='json'
        )
        self.assertTrue(status.is_success(request.status_code))
