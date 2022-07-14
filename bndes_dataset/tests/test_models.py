from django.test import TestCase
from django.db.utils import IntegrityError

from bndes_dataset import models
from bndes_dataset.tests import recipes


class TestBNDESDatasetModel(TestCase):
    """Test case for BNDES Dataset models."""

    def setUp(self):
        """Set up data for tests, created BNDES tag, url and log."""

        self.recipes = recipes.BNDESDatasetRecipes()
        self.tag = self.recipes.tag.make()
        self.url = self.recipes.url.make(tags=[self.tag])
        self.log = self.recipes.log.make(bndes_url=self.url)

    def test_bndes_dataset_models_data_creation(self):
        """Test bndes dataset models data creation"""

        self.assertEqual(models.BNDESLog.objects.count(), 1)
        self.assertEqual(models.BNDESTag.objects.count(), 1)
        self.assertEqual(models.BNDESUrl.objects.count(), 1)

    def test_bndes_dataset_models_str(self):
        """Test bndes dataset models str."""

        self.assertIsInstance(
            models.BNDESUrl.objects.first().__str__(),
            str
        )

        self.assertIsInstance(
            models.BNDESLog.objects.first().__str__(),
            str
        )

        self.assertIsInstance(
            models.BNDESTag.objects.first().__str__(),
            str
        )

    def test_bndes_tag_without_data(self):
        """Test BNDESTag model without data error."""

        with self.assertRaises(IntegrityError):
            self.recipes.tag.make(tag=None)
            self.assertEqual(models.BNDESTag.objects.count(), 1)

    def test_bndes_url_without_data(self):
        """Test BNDESUrl model without data error."""

        with self.assertRaises(IntegrityError):
            self.recipes.url.make(
                tags=None,
                service=None,
                url=None
            )
            self.assertEqual(models.BNDESUrl.objects.count(), 1)

    def test_bndes_log_without_data(self):
        """Test BNDESLog model without data error."""

        with self.assertRaises(IntegrityError):
            self.recipes.log.make(
                response=None,
                params=None,
                bndes_url=self.url,
            )
            self.assertEqual(models.BNDESLog.objects.count(), 1)

    def test_bndes_log_without_foreign_key(self):
        """Test BNDESLog model without url."""

        with self.assertRaises(TypeError):
            self.recipes.log.make(
                bndes_url=None,
            )
            self.assertEqual(models.BNDESLog.objects.count(), 1)
