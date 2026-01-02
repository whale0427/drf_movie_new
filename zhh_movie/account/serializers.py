from djoser.serializers import UserCreateSerializer,UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from .models import Profile

class CustomUniqueValidator(UniqueValidator):

    def __call__(self, value, serializer_field):
        self.message=f"邮箱{value}已存在"
        return super().__call__(value, serializer_field)

class CustomUserCreateSerializer(UserCreateSerializer):
    email=serializers.EmailField(
        validators=[CustomUniqueValidator(queryset=User.objects.all())]
    )
    class Meta:
        model = User
        fields=["id","username","email","password"]

    def create(self, validated_data):
        user=super().create(validated_data)
        profile=Profile(user=user,email=user.email)
        profile.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model=Profile
        fields=("uid","phone","email","avatar","is_upgrade","expire_time")

class UserProfileSerializer(UserSerializer):
    profile=ProfileSerializer(read_only=True)

    class Meta(UserSerializer.Meta):
        fields=(*UserSerializer.Meta.fields,"profile")
