from rest_framework import serializers
from .models import User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserUpdatePasswordSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
