from unittest import mock

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from bndes_dataset.tests import recipes
from bndes_dataset import bndes_requests, models


class TestBNDESDatasetGetView(TestCase):
    """Test case for UserSettings views."""

    def setUp(self):
        """Set up data for tests, created BNDES tag and url."""

        self.recipes = recipes.BNDESDatasetRecipes()
        self.tag = self.recipes.tag.make()
        self.url = self.recipes.url.make(tags=[self.tag])

        self.mock_data_json = {"cpf": "00000000000"}
        self.mock_response_json = [
            {
                "code": 200,
                "code_message": "A requisição foi processada com sucesso.",
                "header": {
                    "api_version": "v2",
                    "service": "mpf/amazonia-protege",
                    "parameters": {
                        "cnpj": "11111111111111"
                    },
                    "client_name": "Minha Empresa",
                    "token_name": "Token de Produção",
                    "billable": True,
                    "price": "0.2",
                    "requested_at": "2021-07-07T08:30:50.000-03:00",
                    "elapsed_time_in_milliseconds": 1854,
                    "remote_ip": "111.111.111.111",
                    "signature": "1czezi3b9UQYcm3VmbDoMIxGyQUH5vQ=="
                },
                "data_count": 1,
                "data": [
                    {
                        "certidao_codigo": "11111111111111111",
                        "conseguiu_emitir_certidao_negativa": False,
                        "emissao_data": "11/11/1111",
                        "mensagem": "Exemplo de texto",
                        "validade_data": "11/11/1111",
                        "site_receipt": "https://www.exemplo.com/exemplo-de-url"
                    }
                ],
                "errors": [],
                "site_receipts": [
                    "https://www.exemplo.com/exemplo-de-url"
                ]
            },
        ]

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
