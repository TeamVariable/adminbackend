"""
admin rest api factoring
"""
from rest_framework import serializers
from rest_framework.response import Response
from visualboard.models import UserInformation, AdminUsers


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInformation
        fields = "__all__"


class AdminInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUsers
        exclude = ("password",)
