from model_mommy.recipe import (
    Recipe,
    foreign_key,
)

from bndes_dataset import models


class BNDESDatasetRecipes:
    """Data recipes to BNDES Dataset model test cases."""

    def __init__(self):

        self.tag = Recipe(
            models.BNDESTag,
            tag='id',
        )

        self.url = Recipe(
            models.BNDESUrl,
            url='https://api.bndes.com/api/v2/consultas/mpf/amazonia-protege',
            service='mpf/amazonia-protege',
            tags=foreign_key(self.tag),
        )

        self.log = Recipe(
            models.BNDESLog,
            response='{"response": "OK"}',
            params='{"id": 1}',
            bndes_url=foreign_key(self.url),
        )
