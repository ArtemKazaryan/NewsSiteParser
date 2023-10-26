from django.contrib import admin
from .models import Resource, Items

# Регистрируем наши модели в админке
admin.site.register(Resource)
admin.site.register(Items)

