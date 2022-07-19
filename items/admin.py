from django.contrib import admin
from .models import Items, Categories
from crum import get_current_user
from django import forms


class ItemsForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ItemsForm, self).__init__(*args, **kwargs)
        user = get_current_user()
        self.fields['category'].queryset = Categories.objects.filter(user=user)


class CategoriesAdmin(admin.ModelAdmin):
    model = Categories
    list_display = ('name', 'total_items')
    search_fields = ('name',)

    def get_queryset(self, request):
        return Categories.objects.filter(user=get_current_user())

    @staticmethod
    def total_items(obj):
        items = Items.objects.filter(category=obj.id).count()
        return '%d' % items


class ItemsAdmin(admin.ModelAdmin):
    #form = ItemsForm
    list_display = ('name', 'category', 'price', 'cost', 'margin')
    #list_filter = ('category',)
    search_fields = ('name',)

    def get_queryset(self, request):
        return Items.objects.filter(user=get_current_user())

    @staticmethod
    def margin(obj):
        if obj.cost.amount == 0:
            return '%3.2f%%' % 100
        else:
            return '%3.2f%%' % (((obj.price.amount - obj.cost.amount) / obj.price.amount) * 100)


admin.site.register(Items, ItemsAdmin)
admin.site.register(Categories, CategoriesAdmin)