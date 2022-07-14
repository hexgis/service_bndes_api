import aiohttp
import asyncio
import requests

from datetime import datetime, timedelta

from django.conf import settings

from bndes_dataset import models, serializers


class BNDES:

    response = []

    @staticmethod
    def get_bndes_data(request):
        """Get all BNDES information avaliable
        with requested data from defined environment
        variables

        Args:
            request (HTTP request): HTTP request

        Returns:
            response (list): list of every response made
        """

        params = request.data

        urls = BNDES.get_possible_urls(params)

        response, urls = BNDES.verify_logs(urls, params)

        if len(urls) != 0:
            asyncio.run(BNDES.request_call_async(urls, params))
            if len(BNDES.response) != 0:
                BNDES.store_bndes_response(
                    BNDES.response,
                    params
                )

        response = response + BNDES.response
        BNDES.response = []

        return response

    @classmethod
    def get_possible_urls(cls, params):
        """Method for getting possible urls with given parameters.

        Args:
            params (JSON): user request params.

        Returns:
            (list): List of filtered BNDESUrl.
        """

        urls = []
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
                urls.append(bndes_url)

        return urls

    @classmethod
    def verify_logs(cls, urls, params):
        """Method for filtering possible BNDESLog if exists, or
        showing the url that needs to be requested on bndes.

        Args:
            urls (list): BNDES.get_possible_urls method results.
            params (JSON): User request params.

        Returns:
            response (list): List of possible BNDESLog with given
            params.
            urls_response (list): List of BNDESUrl url for requesting.
        """

        response = []
        urls_response = []
        for url in urls:
            bndes_log = models.BNDESLog.objects.filter(
                params=params,
                date_created__gt=(
                    datetime.now() - timedelta(url.validity_in_days)
                ).isoformat()
            ).last()
            if bndes_log:
                response.append(bndes_log.response)
        urls_response.append(url.url)

        return response, urls_response

    @classmethod
    async def post_request(cls, session, url, params):
        """ Method to post request calls asynchronously
        using aioHTTP session.

        Args:
            urls (list): list of BNDES endpoints urls.
            params (JSON): user request params.

        Returns:
            response_json (JSON): BNDES result for instance params.
        """

        async with session.post(url, params=params) as response:
            response_json = await response.json()
            return response_json

    @classmethod
    async def request_call_async(cls, urls, params):
        """ Method to run request list concurrently
        using aioHTTP.

        Args:
            urls (list): list of BNDES endpoints urls.
            params (JSON): user request params.
        """

        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in urls:
                tasks.append(
                    asyncio.ensure_future(
                        BNDES.post_request(session, url, params)
                    )
                )

            response_list = await asyncio.gather(*tasks)

            for response_json in response_list:
                BNDES.response.append(response_json)

    @classmethod
    def store_bndes_response(cls, response_list, params):
        """Method for storing bndes responses in BNDESLog model.

        Args:
            response_list (list): BNDES responses.
            params (dict): User requested params.
        """

        for response in response_list:
            if response.get("code") in settings.BNDES_ACCEPTABLE_HTTP_CODES:
                serializer_data = {}
                serializer_data["response"] = response
                serializer_data["params"] = params
                serializer_data["bndes_url"] = models.BNDESUrl.objects.filter(
                    service=response.get("header").get("service")
                ).last().pk
                serializer = serializers.BNDESLogSerializer(
                    data=serializer_data
                )

                serializer.is_valid()
                serializer.save()
