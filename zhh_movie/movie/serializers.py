from rest_framework import serializers
from .models import Movie, Category


# class MovieListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Movie
#         fields="__all__"
#
# class MovieDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Movie
#         fields="__all__"
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model=Movie
        fields="__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields="__all__"