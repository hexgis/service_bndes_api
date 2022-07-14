from django.contrib.gis import admin

from bndes_dataset import models


class BNDESTagAdmin(admin.ModelAdmin):
    """Admin class for UserSettings data."""

    list_display = ('tag',)

    fields = ('tag',)

    search_fields = ('tag',)

    filter_fields = ('tag',)


class BNDESUrlAdmin(admin.ModelAdmin):
    """Admin class for UserSettings data."""

    list_display = (
        'url',
    )

    fields = (
        'url',
        'tags',
    )

    search_fields = (
        'url',
        'tags'
    )

    filter_fields = (
        'url',
        'tags'
    )


admin.site.register(models.BNDESUrl, BNDESUrlAdmin)
admin.site.register(models.BNDESTag, BNDESTagAdmin)
