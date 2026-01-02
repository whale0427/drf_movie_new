from django.contrib import admin
from .models import Category,Movie

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","category_name",)
    search_fields= ("category_name",)
admin.site.register(Category,CategoryAdmin)

class MovieAdmin(admin.ModelAdmin):
    list_display = ("id","movie_name","release_year","release_date","director")
    search_fields= ("movie_name","director")
    list_display_links = ("movie_name",)
    list_filter = ("category",)
admin.site.register(Movie,MovieAdmin)