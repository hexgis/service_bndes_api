import requests
import urllib

from datetime import datetime, timedelta

from bndes_dataset import models, serializers


class BNDES:
    """BNDES request handler data from transparency API."""

    response = None

    @staticmethod
    def get_bndes_data(request) -> dict:
        """Get all BNDES information avaliable
        with requested data from defined environment
        variables.

        Args:
            request (HTTP request): HTTP request.

        Returns:
            dict: BNDES requested response.
        """

        url = BNDES.get_url(request.data)

        response, request_url = BNDES.verify_logs(url, request.data)

        if request_url:
            try:
                BNDES.get_request(request_url)
            except Exception as exc:
                response.status_code = 500
                response.data = {
                    'error': f'Error while getting data from {url} - {exc}'
                }

            if BNDES.response:
                BNDES.store_bndes_response(
                    BNDES.response,
                    request.data,
                    url.pk
                )

        if BNDES.response:
            response = BNDES.response
            BNDES.response = None

        return response

    @classmethod
    def get_url(cls, params: dict) -> dict:
        """Method for get url with given parameters.

        Args:
            params (dict): user request params.

        Returns:
            dict: Filtered BNDESUrl.
        """

        if params.get('cpf'):
            params['id'] = params.get('cpf')
        elif params.get('cnpj'):
            params['id'] = params.get('cnpj')

        for bndes_url in models.BNDESUrl.objects.all():
            if not bndes_url.tags.exclude(
                pk__in=models.BNDESTag.objects.filter(
                    tag__in=list(params.keys())
                )
            ):
                url = bndes_url

        return url

    @classmethod
    def get_request(cls, url: str):
        """Method to send request to given url
        and store in BNDES.response global variable.

        Args:
            urls (str): BNDES endpoint url.

        Raises:

        """

        json_response = requests.get(url, timeout=(5, 10)).json()

        if (
            len(json_response.get('operacoes')) != 0 or
            len(json_response.get('desembolsos')) != 0 or
            len(json_response.get('carteira')) != 0
        ):
            BNDES.response = json_response

    @classmethod
    def verify_logs(cls, url: dict, params: dict) -> dict:
        """Method for filtering possible BNDESLog if exists, or
        showing the url that needs to be requested on bndes.

        Args:
            url (dict): BNDES.get_url method result.
            params (dict): User request params.

        Returns:
            dict: BNDESLog of given params or request_url.
        """

        response = None
        request_url = None

        bndes_log = models.BNDESLog.objects.filter(
            params=params,
            date_created__gt=(
                datetime.now() - timedelta(url.validity_in_days)
            ).isoformat()
        ).last()

        if bndes_log:
            response = bndes_log.response
        else:
            request_url = urllib.parse.urljoin(url.url, params.get('id'))

        return response, request_url

    @classmethod
    def store_bndes_response(cls, response: dict, params: dict, url_pk: int):
        """Method for storing BNDES responses in BNDESLog model.

        Args:
            response (dict): BNDES response.
            params (dict): User requested params.
            url_pk (int): BNDESUrl pk.
        """

        serializer_data = {}
        serializer_data['response'] = response
        serializer_data['params'] = params
        serializer_data['bndes_url'] = models.BNDESUrl.objects.get(
            pk=url_pk
        ).pk
        serializer = serializers.BNDESLogSerializer(
            data=serializer_data
        )

        serializer.is_valid()
        serializer.save()
