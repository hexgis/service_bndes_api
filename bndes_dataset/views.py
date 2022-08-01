from django.http import JsonResponse

from rest_framework import (
    generics,
    permissions,
    response,
    status
)

from bndes_dataset.bndes_requests import BNDES


class AuthModelMixIn:
    """"Authentication Model MixIn for UserProfile views.

    Default permission_classes for permissions.AllowAny.
    """

    permission_classes = (permissions.AllowAny,)


class BNDESDatasetGetView(AuthModelMixIn, generics.GenericAPIView):
    """View to get BNDES data.

    Args:
        request (dict): HTTP request data

    Returns:
        dict: query results
    """

    def post(self, request):
        """Get BNDES data.

        Args:
            request (dict): HTTP request data.

        Returns:
            response.Response: BNDES serialized results.
        """

        bndes_response = BNDES.get_bndes_data(request)

        if bndes_response:
            return JsonResponse(bndes_response, safe=False)
        else:
            return response.Response(
                f'Error while trying to retrieve data from: {request.data}',
                status.HTTP_404_NOT_FOUND
            )
