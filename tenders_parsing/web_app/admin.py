from django.contrib import admin

from .filters import PriceRangeFilter
from .models import ObjectType, Region, Tender, TenderType


@admin.register(ObjectType)
class ObjectTypeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name'
    )


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name'
    )


@admin.register(TenderType)
class TenderTypeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name'
    )


@admin.register(Tender)
class TenderAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'tender_type',
        'number',
        'title',
        'price',
        'organizer',
        'customer',
        'start_date',
        'end_date',
        'object_type',
        'region'
    )
    list_filter = (
        'start_date',
        'end_date',
        PriceRangeFilter,
        'tender_type',
        'object_type',
        'region'
    )
    search_fields = ('number', 'title')
