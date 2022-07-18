import aiohttp
import asyncio
import requests

from datetime import datetime, timedelta

from django.conf import settings

from bndes_dataset import models, serializers


class BNDES:

    response = None

    @staticmethod
    def get_bndes_data(request):
        """Get all BNDES information avaliable
        with requested data from defined environment
        variables.

        Args:
            request (HTTP request): HTTP request.

        Returns:
            response (dict): BNDES requested response.
        """

        params = request.data

        url = BNDES.get_url(params)
        url_pk = url.pk

        response, url = BNDES.verify_logs(url, params)

        if url:
            BNDES.get_request(url)
            if BNDES.response:
                BNDES.store_bndes_response(
                    BNDES.response,
                    params,
                    url_pk
                )

        if BNDES.response:
            response = BNDES.response
            BNDES.response = None

        return response

    @classmethod
    def get_url(cls, params):
        """Method for get url with given parameters.

        Args:
            params (JSON): user request params.

        Returns:
            (dict): Filtered BNDESUrl.
        """

        if params.get("cpf"):
            params["id"] = params.get("cpf")
        elif params.get("cnpj"):
            params["id"] = params.get("cnpj")

        for bndes_url in models.BNDESUrl.objects.all():
            if not bndes_url.tags.exclude(
                pk__in=models.BNDESTag.objects.filter(
                    tag__in=list(params.keys())
                )
            ):
                url = bndes_url

        return url

    @classmethod
    def verify_logs(cls, url, params):
        """Method for filtering possible BNDESLog if exists, or
        showing the url that needs to be requested on bndes.

        Args:
            url (dict): BNDES.get_url method result.
            params (JSON): User request params.

        Returns:
            response (dict): BNDESLog of given params.
            url_response (str): BNDESUrl url for requesting.
        """

        response = None
        url_response = None
        bndes_log = models.BNDESLog.objects.filter(
            params=params,
            date_created__gt=(
                datetime.now() - timedelta(url.validity_in_days)
            ).isoformat()
        ).last()

        if bndes_log:
            response = bndes_log.response
        else:
            url_response = url.url + params.get("id")

        return response, url_response

    @classmethod
    def get_request(cls, url):
        """ Method to send request to given url
        and store in BNDES.response global variable.

        Args:
            urls (str): BNDES endpoint url.

        """

        response = requests.get(url).json()
        if (
            len(response.get("operacoes")) != 0 or
            len(response.get("desembolsos")) != 0 or
            len(response.get("carteira")) != 0
        ):
            BNDES.response = response

    @classmethod
    def store_bndes_response(cls, response, params, url_pk):
        """Method for storing BNDES responses in BNDESLog model.

        Args:
            response (dict): BNDES response.
            params (dict): User requested params.
            url_pk (int): BNDESUrl pk.
        """

        serializer_data = {}
        serializer_data["response"] = response
        serializer_data["params"] = params
        serializer_data["bndes_url"] = models.BNDESUrl.objects.get(
            pk=url_pk
        ).pk
        serializer = serializers.BNDESLogSerializer(
            data=serializer_data
        )

        serializer.is_valid()
        serializer.save()
