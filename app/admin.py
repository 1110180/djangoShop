from django.contrib import admin
from app.models import *
admin.site.register(Tovar)


@admin.register(Cart)
class CarAdmin(admin.ModelAdmin):
    list_display = ('user', 'tovar', 'count', 'summa')

