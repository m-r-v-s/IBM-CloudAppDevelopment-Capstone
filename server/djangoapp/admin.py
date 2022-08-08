from django.contrib import admin
from .models import CarMake, CarModel


 
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5


# CarModelAdmin class

class CarModelAdmin(admin.ModelAdmin):
    list_display = ["make", "name", "type", "year"]
    list_filter = ["year"]
    search_fields = ["name"]


# CarMakeAdmin class with CarModelInline

class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ["name", "description"]


# Register models here
