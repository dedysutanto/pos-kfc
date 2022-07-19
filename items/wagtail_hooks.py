from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from .models import Items, Categories
from crum import get_current_user
from wagtail.admin.forms.models import WagtailAdminModelForm


class ItemsForm(WagtailAdminModelForm):
    class Meta:
        model = Items
        fields = '__all__'

    def __init__(self):
        super(ItemsForm, self).__init__(*args, **kwargs)
        self.fields['category'] = Categories.objects.filter(user=get_current_user())


class CategoriesAdmin(ModelAdmin):
    model = Categories
    menu_label = 'Categories'  # ditch this to use verbose_name_plural from model
    menu_icon = 'list-ul'  # change as required
    #menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('name', 'total_items')
    #list_filter = ('name',)
    search_fields = ('name',)

    @staticmethod
    def total_items(obj):
        items = Items.objects.filter(category=obj.id).count()
        return '%d' % items

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Only show people managed by the current user
        return qs.filter(user=request.user)
        #return Categories.objects.filter(user=get_current_user())


class ItemsAdmin(ModelAdmin):
    model = Items
    menu_label = 'Items'  # ditch this to use verbose_name_plural from model
    menu_icon = 'tag'  # change as required
    #menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('name', 'category', 'price', 'cost', 'margin')
    #list_filter = ('category',)
    search_fields = ('name',)

    base_form_class = ItemsForm

    @staticmethod
    def margin(self):
        if self.cost.amount == 0:
            return '%3.2f%%' % 100
        else:
            return '%3.2f%%' % (((self.price.amount - self.cost.amount) / self.price.amount) * 100)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Only show people managed by the current user
        return qs.filter(user=request.user)
        #return Items.objects.filter(user=get_current_user())


class ItemsGroup(ModelAdminGroup):
    menu_label = 'Items'
    menu_icon = 'folder-open-inverse'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (ItemsAdmin, CategoriesAdmin)


modeladmin_register(ItemsGroup)