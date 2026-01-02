from rest_framework import serializers
from .models import Card,Order
from account.models import Profile
from account.serializers import ProfileSerializer

class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model=Card
        fields=["id","card_name","card_price","duration","info"]

class AlipaySerializer(serializers.ModelSerializer):
    profile=ProfileSerializer(read_only=True)
    class Meta:
        model=Order
        fields=["id","card_name","card_price","duration","info","profile"]

class OrderSerializer(serializers.ModelSerializer):
    pay_type_display = serializers.CharField(source='get_pay_type_display', read_only=True)
    pay_status_display=serializers.CharField(source="get_pay_status_display",read_only=True)
    card_name=serializers.CharField(source="card.card_name",read_only=True)
    card_info = serializers.CharField(source="card.info", read_only=True)
    class Meta:
        model=Order
        fields="__all__"