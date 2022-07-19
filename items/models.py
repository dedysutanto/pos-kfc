from django.db import models
from django.contrib.auth.models import User
from crum import get_current_user
from djmoney.models.fields import MoneyField
from django.utils.translation import gettext as _
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel


class Categories(models.Model):
    name = models.CharField(_('Category Name'), max_length=20, unique=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    panels = [
        FieldPanel('name'),
    ]

    class Meta:
        db_table = 'categories'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return '%s' % self.name

    def save(self):
        self.user = get_current_user()
        return super(Categories, self).save()


class Items(models.Model):
    def limit_choices_to_current_user():
        user = get_current_user()
        return {'user': user}

    name = models.CharField(_('Item Name'), max_length=20, unique=True)
    description = models.TextField(_('Description'), blank=True)
    category = models.ForeignKey(
        Categories,
        on_delete=models.RESTRICT,
        verbose_name=_('Category'),
        limit_choices_to=limit_choices_to_current_user,
    )
    price = MoneyField(max_digits=19, decimal_places=2, default=0, default_currency='IDR')
    cost = MoneyField(max_digits=19, decimal_places=2, default=0, default_currency='IDR')
    is_available = models.BooleanField(_('Available to sell'), default=True)

    sku = models.CharField(_('SKU'), max_length=50, blank=True)
    barcode = models.CharField(_('Barcode'), max_length=50, blank=True)

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        MultiFieldPanel([FieldPanel('name'), FieldPanel('description')], heading=_('Name and Description')),
        FieldPanel('category'),
        MultiFieldPanel([FieldPanel('price'), FieldPanel('cost')], heading=_('Price and Cost')),
        FieldPanel('is_available'),
        MultiFieldPanel([FieldPanel('sku'), FieldPanel('barcode')], heading=_('SKU and Barcode')),
        ImageChooserPanel('image'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        db_table = 'items'
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self):
        return '%s' % self.name

    def save(self):
        self.user = get_current_user()
        return super(Items, self).save()

