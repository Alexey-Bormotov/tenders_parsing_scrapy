from admin_numeric_filter.admin import RangeNumericFilter
from django.contrib import admin

from .models import Customer, ObjectType, Organizer, Region, Tender, TenderType


@admin.register(TenderType)
class TenderTypeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name'
    )


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name'
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name'
    )


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
        ('price', RangeNumericFilter),
        'tender_type',
        'object_type',
        'region'
    )
    search_fields = ('number', 'title')
