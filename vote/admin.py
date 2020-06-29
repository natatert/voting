from django.contrib import admin

# Register your models here.
from .models import Character, Vote


admin.site.register(Character)
admin.site.register(Vote)
