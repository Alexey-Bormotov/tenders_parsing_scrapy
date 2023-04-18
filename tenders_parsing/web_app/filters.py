from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class PriceRangeFilter(admin.SimpleListFilter):
    title = _('Сумма закупки')
    parameter_name = 'price_range'

    def lookups(self, request, model_admin):
        return (
            ('1', _('0-999.999 руб.')),
            ('2', _('1.000.000-9.999.999 руб.')),
            ('3', _('>= 10.000.000 руб.')),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(
                price__gte=0,
                price__lt=1_000_000,
            )
        if self.value() == '2':
            return queryset.filter(
                price__gte=1_000_000,
                price__lt=10_000_000,
            )
        if self.value() == '3':
            return queryset.filter(
                price__gte=10_000_000,
            )
