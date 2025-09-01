from django.contrib import admin
from .models import PointOfInterest

@admin.register(PointOfInterest)
class PointOfInterestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'external_id', 'category', 'average_rating')
    list_filter = ('category',)
    search_fields = ('id', 'external_id', 'name')
    readonly_fields = ('average_rating',)