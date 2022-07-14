from django.http import JsonResponse

from rest_framework import (
    generics,
    permissions
)

from bndes_dataset.bndes_requests import BNDES


class AuthModelMixIn:
    """"Authentication Model MixIn for UserProfile views.
        Default permission_classes for permissions.IsAuthenticated.
    """

    permission_classes = (permissions.AllowAny,)


class BNDESDatasetGetView(AuthModelMixIn, generics.GenericAPIView):
    """View to get BNDES data.

    Args:
        request.data (JSON): HTTP request data

    Returns:
        dict: query results
    """

    def post(self, request):
        """Get BNDES data.

        Args:
            request.data (JSON): HTTP request data

        Returns:
            ReturnDict: BNDES serialized results
        """

        response = BNDES.get_bndes_data(request)
        return JsonResponse(response, safe=False)
