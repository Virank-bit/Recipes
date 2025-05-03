from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(User)
class ShowUser(admin.ModelAdmin):
    list_display=["name","email","password","phone","gender","timestamp"]

@admin.register(Favourite)
class ShowFavourite(admin.ModelAdmin):
    list_display=["user","recipe"]