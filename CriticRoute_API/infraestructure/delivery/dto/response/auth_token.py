from dataclasses import dataclass

from rest_framework import serializers


@dataclass
class AuthToken:
    refresh: str
    access: str


class AuthSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
