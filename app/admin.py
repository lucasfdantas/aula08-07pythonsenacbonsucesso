from django.contrib import admin
from .models import Usuarios




# Register your models here.
@admin.register(Usuarios)
class PersonAdmin(admin.ModelAdmin):
    pass