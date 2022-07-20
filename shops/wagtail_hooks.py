from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from .models import Shops, Cashiers
from crum import get_current_user


class ShopsAdmin(ModelAdmin):
    model = Shops
    menu_label = 'Shops'  # ditch this to use verbose_name_plural from model
    menu_icon = 'home'  # change as required
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('name', 'address', 'number_cashiers')
    #list_filter = ('name',)
    search_fields = ('name',)

    @staticmethod
    def number_cashiers(obj):
        cashiers = Cashiers.objects.filter(shop=obj.id).count()

        return '%d' % cashiers

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Only show people managed by the current user
        return qs.filter(user=request.user)
        #return Shops.objects.filter(user=get_current_user())


class CashiersAdmin(ModelAdmin):
    model = Cashiers
    menu_label = 'Cashiers'  # ditch this to use verbose_name_plural from model
    menu_icon = 'tag'  # change as required
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('name', 'shop', 'is_active')
    #list_filter = ('shop',)
    search_fields = ('name', 'shop__name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Only show people managed by the current user
        return qs.filter(user=request.user)
        #return Cashiers.objects.filter(user=get_current_user())


class ShopsGroup(ModelAdminGroup):
    menu_label = 'Shops'
    menu_icon = 'folder-open-inverse'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (ShopsAdmin, CashiersAdmin)

# Now you just need to register your customised ModelAdmin class with Wagtail
#modeladmin_register(ItemsAdmin)

# When using a ModelAdminGroup class to group several ModelAdmin classes together,
# you only need to register the ModelAdminGroup class with Wagtail:
modeladmin_register(ShopsGroup)