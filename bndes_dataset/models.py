from django.db import models
from django.conf import settings


class BNDESTag(models.Model):
    """Model to store user BNDES tag.

    * Association:
        * Has many :model:`bndes_dataset.BNDESUrl`.
    """

    tag = models.CharField(max_length=255)

    def __str__(self):
        """Model class string.

        Returns:
            str: short description of model.
        """

        return f'{self.tag}'

    class Meta:
        app_label = 'bndes_dataset'
        verbose_name = 'BNDES Tag'
        ordering = ('-tag', )


class BNDESUrl(models.Model):
    """Model to store user BNDES url.

    * Association:
        * Has many :model:`bndes_dataset.BNDESTag`.
    """

    url = models.CharField(max_length=255)

    service = models.CharField(max_length=255)

    tags = models.ManyToManyField(
        BNDESTag,
        related_name='urls',
    )

    validity_in_days = models.IntegerField(
        default=settings.BNDES_URL_VALIDITY
    )

    def __str__(self):
        """Model class string.

        Returns:
            str: short description of model.
        """

        return f'{self.url}'

    class Meta:
        app_label = 'bndes_dataset'
        verbose_name = 'BNDES url'
        ordering = ('-url', )


class BNDESLog(models.Model):
    """Model to store user BNDES logs.

    * Association:
        * Has no association.
    """

    response = models.JSONField()

    date_created = models.DateTimeField(auto_now_add=True)

    params = models.JSONField()

    bndes_url = models.ForeignKey(
        BNDESUrl,
        on_delete=models.CASCADE,
        related_name='bndes_url',
    )

    def __str__(self):
        """Model class string.

        Returns:
            str: short description of model.
        """

        return f'{self.response}'

    class Meta:
        app_label = 'bndes_dataset'
        verbose_name = 'BNDES Log'
        ordering = ('date_created', )
