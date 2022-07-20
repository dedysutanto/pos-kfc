from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from .models import Receipts, Sales
from crum import get_current_user


class ReceiptsAdmin(ModelAdmin):
    model = Receipts
    menu_label = 'Receipts'  # ditch this to use verbose_name_plural from model
    menu_icon = 'form'  # change as required
    #menu_order = 300  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('created_at', '__str__', 'cashier', 'shop', 'total_amount',)
    #list_filter = ('name',)
    #search_fields = ('__str__',)

    def get_queryset(self, request):
        return Receipts.objects.filter(user=get_current_user())

    @staticmethod
    def total_amount(self):
        sales = Sales.objects.filter(receipt=self.id, user=self.user)
        total_sales = 0
        if sales:
            for sale in sales:
                total_sales += sale.item.price * sale.amount

        return total_sales


class SalesAdmin(ModelAdmin):
    model = Sales
    menu_label = 'Sales'  # ditch this to use verbose_name_plural from model
    menu_icon = 'tag'  # change as required
    #menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('created_at', 'item', 'category', 'amount', 'receipt')
    #list_filter = ('category',)
    #search_fields = ('name',)

    def get_queryset(self, request):
        return Sales.objects.filter(user=get_current_user())


class SalesGroup(ModelAdminGroup):
    menu_label = 'Sales'
    menu_icon = 'folder-open-inverse'  # change as required
    menu_order = 500  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (ReceiptsAdmin, SalesAdmin)

# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(SalesGroup)
