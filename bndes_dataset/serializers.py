from rest_framework import serializers

from bndes_dataset import models


class BNDESUrlSerializer(serializers.ModelSerializer):
    """Class to serialize `models.BNDESUrl` model data."""

    class Meta:
        model = models.BNDESUrl
        fields = '__all__'
        depth = 1


class BNDESLogSerializer(serializers.ModelSerializer):
    """Class to serialize `models.BNDESLog` model data."""

    def create(self, validated_data):
        """Method for saving BNDESLog serialized data
        on database.

        Args:
            validated_data (dict): BNDESLog serialized data

        Returns:
            dict: BNDESLog serialized data
        """

        response_log = models.BNDESLog.objects.create(**validated_data)
        response_log.save()
        return response_log

    class Meta:
        model = models.BNDESLog
        fields = (
            'response',
            'bndes_url',
            'params',
        )
