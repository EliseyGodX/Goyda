from django.contrib import admin
from core.models import Country, Region, City

admin.site.register((Country, Region, City))
