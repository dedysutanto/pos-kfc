from django.contrib import admin
from .models import Shops, Cashiers
from crum import get_current_user


@admin.register(Shops)
class ShopsAdmin(admin.ModelAdmin):
    model = Shops
    list_display = ('name', 'address', 'number_cashiers')
    #list_filter = ('name',)
    search_fields = ('name',)

    @staticmethod
    def number_cashiers(obj):
        cashiers = Cashiers.objects.filter(shop=obj.id).count()

        return '%d' % cashiers

    def get_queryset(self, request):
        return Shops.objects.filter(user=get_current_user())


@admin.register(Cashiers)
class CashiersAdmin(admin.ModelAdmin):
    model = Cashiers
    list_display = ('name', 'shop')
    #list_filter = ('shop',)
    search_fields = ('name', 'shop__name')

    def get_queryset(self, request):
        return Cashiers.objects.filter(user=get_current_user())



#admin.site.register(Shops, ShopsAdmin)
#admin.site.register(Cashiers, CashiersAdmin)