from django.contrib import admin

from .models import Card,Order


# Register your models here.
class CardAdmin(admin.ModelAdmin):
    search_fields=("card_name",)
admin.site.register(Card, CardAdmin)

class OrderAdmin(admin.ModelAdmin):
    search_fields=("order_sn",)
admin.site.register(Order, OrderAdmin)