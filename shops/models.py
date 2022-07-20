from django.db import models
from django.contrib.auth.models import User
from crum import get_current_user
from django.utils.translation import gettext as _
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


class Shops(models.Model):
    name = models.CharField(_('Shop Name'), max_length=30, unique=True)
    description = models.TextField(_('Description'), blank=True)
    address = models.CharField(_('Address'), max_length=100, blank=True)
    telephone = models.CharField(_('Telephone'), max_length=50, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    panels = [
        MultiFieldPanel([FieldPanel('name'), FieldPanel('description')], heading=_('Name and Description')),
        FieldPanel('address'),
        FieldPanel('telephone'),
    ]

    class Meta:
        db_table = 'shops'
        verbose_name = 'shop'
        verbose_name_plural = 'shops'

    def __str__(self):
        return '%s' % self.name

    def save(self):
        self.user = get_current_user()
        return super(Shops, self).save()


class Cashiers(models.Model):
    def limit_choices_to_current_user():
        user = get_current_user()
        return {'user': user}

    name = models.CharField(_('Cashier Name'), max_length=30, unique=True)
    shop = models.ForeignKey(
        Shops,
        on_delete=models.RESTRICT,
        verbose_name=_('Shop'),
        limit_choices_to=limit_choices_to_current_user,
    )
    is_active = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    panels = [
        FieldPanel('name'),
        FieldPanel('shop'),
    ]

    class Meta:
        db_table = 'cashiers'
        verbose_name = 'cashier'
        verbose_name_plural = 'cashiers'

    def __str__(self):
        return '%s' % self.name

    def save(self):
        self.user = get_current_user()
        return super(Cashiers, self).save()
    