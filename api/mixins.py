from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.response import Response

# from rest_framework_simplejwt.authentication import JWTAuthentication

CONTENT_TYPE_JSON = "application/json"


class UserFilteredMixin(generics.GenericAPIView):
    """
    Mixin to filter queryset by the current user.
    """

    def get_queryset(self):
        """
        Returns the queryset filtered by the current user.
        """
        response = super().get_queryset().filter(user=self.request.user)
        return response

    def perform_create(self, serializer):
        """
        Saves the serializer with the current user.
        """
        serializer.save(user=self.request.user)

class ContentTypeValidationMixin:
    """
    Mixin to validate Content-Type header for JSON requests.
    """

    def validate_content_type(self, request):
        """
        Validates that the Content-Type header is application/json.
        """
        if request.content_type != CONTENT_TYPE_JSON:
            return Response(
                {"detail": "Content-Type must be application/json"},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )
        return None