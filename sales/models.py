from django.db import models
from django.contrib.auth.models import User
from items.models import Items, Categories
from shops.models import Cashiers, Shops
from django.utils.translation import gettext as _
from crum import get_current_user
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


class Receipts(models.Model):
    def limit_choices_to_current_user():
        user = get_current_user()
        return {'user': user}

    #total_amount = models.IntegerField(_('Total Amount'), default=0)
    cashier = models.ForeignKey(
        Cashiers,
        on_delete=models.RESTRICT,
        verbose_name=_('Cashier'),
        limit_choices_to=limit_choices_to_current_user,
    )
    shop = models.ForeignKey(
        Shops,
        on_delete=models.RESTRICT,
        verbose_name=_('Shop'),
        limit_choices_to=limit_choices_to_current_user,
    )

    panels = [
        FieldPanel('cashier'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'receipts'
        verbose_name = 'receipt'
        verbose_name_plural = 'receipts'

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return '#%d' % self.id

    def save(self):
        self.user = self.cashier.user
        self.shop = self.cashier.shop
        return super(Receipts, self).save()


class Sales(models.Model):
    def limit_choices_to_current_user():
        user = get_current_user()
        return {'user': user}

    amount = models.IntegerField(_('Amount'), default=1)
    receipt = models.ForeignKey(
        Receipts,
        on_delete=models.RESTRICT,
        verbose_name=_('Receipt'),
        limit_choices_to=limit_choices_to_current_user,
    )
    item = models.ForeignKey(
        Items,
        on_delete=models.RESTRICT,
        verbose_name=_('Item'),
        limit_choices_to=limit_choices_to_current_user,
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.RESTRICT,
        verbose_name=_('Category'),
        limit_choices_to=limit_choices_to_current_user,
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    panels = [
        FieldPanel('receipt'),
        MultiFieldPanel([FieldPanel('item'), FieldPanel('amount')], heading=_('Item Sale')),
    ]

    class Meta:
        db_table = 'sales'
        verbose_name = 'sale'
        verbose_name_plural = 'sales'

    def __str__(self):
        return '#%d' % self.id

    def save(self):
        self.user = self.item.user
        self.category = self.item.category
        return super(Sales, self).save()
