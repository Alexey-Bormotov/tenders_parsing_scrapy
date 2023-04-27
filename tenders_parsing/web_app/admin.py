from admin_numeric_filter.admin import RangeNumericFilter
from django.contrib import admin

from .models import (
    JuridicalPerson, ObjectType, Region, Tender, TenderType, TenderItem
)


@admin.register(TenderType)
class TenderTypeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name'
    )


@admin.register(JuridicalPerson)
class JuridicalPersonAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'short_name',
        'registration_date',
        'inn',
        'ogrn',
        'kpp',
        'web_site',
        'eis_number',
        'telephone',
        'email',
        'fax',
        'contact_person',
        'address',
        'region'
    )
    list_filter = ('region',)
    search_fields = ('name', 'short_name', 'inn')


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
        'customer_region'
    )
    list_filter = (
        'start_date',
        'end_date',
        ('price', RangeNumericFilter),
        'tender_type',
        'object_type',
        'customer_region'
    )
    search_fields = ('number', 'title')


@admin.register(TenderItem)
class TenderItemAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'code',
        'title',
        'quantity',
        'price',
        'tender'
    )
    list_filter = (
        ('price', RangeNumericFilter),
    )
    search_fields = ('code', 'title', 'tender__number')
