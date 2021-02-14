# django imports
from rest_framework import serializers


class UserLoginRequestSerializer(serializers.Serializer):
    """
    UserLoginSerializer
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)