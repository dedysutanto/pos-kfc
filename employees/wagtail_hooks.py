from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from .models import Employees
from crum import get_current_user


class EmployeesAdmin(ModelAdmin):
    model = Employees
    menu_label = 'Employees'  # ditch this to use verbose_name_plural from model
    menu_icon = 'user'  # change as required
    menu_order = 300  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('name', 'email',)
    #list_filter = ('name',)
    search_fields = ('name',)

    def get_queryset(self, request):
        return Employees.objects.filter(user=get_current_user())


# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(EmployeesAdmin)

# When using a ModelAdminGroup class to group several ModelAdmin classes together,
# you only need to register the ModelAdminGroup class with Wagtail:
#modeladmin_register(ItemsGroup)