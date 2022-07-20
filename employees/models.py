import random
from django.db import models
from django import forms
from django.contrib.auth.models import User
from shops.models import Shops
from crum import get_current_user
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from django.utils.translation import gettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


class Rights(models.Model):
    name = models.CharField(_('Access Right Name'), max_length=50)
    backoffice = models.BooleanField(_('Back Office Access'), default=True)
    cashier = models.BooleanField(_('Cashier Access'), default=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_owner = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    panels = [
        FieldPanel('name'),
        MultiFieldPanel([FieldPanel('backoffice'), FieldPanel('cashier')],
                        heading=_('Access Rights')),
    ]

    class Meta:
        db_table = 'rights'
        verbose_name = 'access Right'
        verbose_name_plural = 'access Rights'

    def __str__(self):
        return '%s' % self.name

    def save(self):
        if self.user is None:
            self.user = get_current_user()
        return super(Rights, self).save()


class Employees(models.Model):
    def limit_choices_to_current_user():
        user = get_current_user()
        return {'user': user}

    name = models.CharField(_('Employee Name'), max_length=50)
    email = models.EmailField(_('Email'))
    telephone = models.CharField(_('Telephone'), max_length=50, blank=True)
    pin = models.CharField(_('Cashier PIN'), max_length=4)
    shops = models.ManyToManyField(
        Shops,
        limit_choices_to=limit_choices_to_current_user,
        verbose_name=_('Shops'),
    )

    right = models.ForeignKey(
        Rights,
        on_delete=models.RESTRICT,
        limit_choices_to=limit_choices_to_current_user,
        verbose_name=_('Access Right')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    panels = [
        MultiFieldPanel([FieldPanel('name'), FieldPanel('email'), FieldPanel('telephone')],
                        heading=_('Name, Email and Telephone')),
        MultiFieldPanel([FieldPanel('right'), FieldPanel('pin')],
                        heading=_('Access Right and PIN')),
        FieldPanel('shops', widget=forms.CheckboxSelectMultiple(attrs={"checked":""})),
    ]

    class Meta:
        db_table = 'employees'
        verbose_name = 'employee'
        verbose_name_plural = 'employees'

    def __str__(self):
        return '%s' % self.name

    def save(self):
        if self.user is None:
            self.user = get_current_user()
        return super(Employees, self).save()


def create_initial_access_right(obj):
    # Create Owner Right
    right_owner = Rights()
    right_owner.name = 'Owner'
    right_owner.user = obj
    right_owner.is_owner = True
    right_owner.save()

    # Create Cashier Right
    right_cashier = Rights()
    right_cashier.name = 'Cashier'
    right_cashier.backoffice = False
    right_cashier.user = obj
    right_cashier.save()


def create_first_employee(obj):
    right = Rights.objects.get(is_owner=True, user=obj)
    emp = Employees()
    emp.name = obj.username
    emp.email = obj.email
    emp.pin = f'{random.randrange(1, 10**4):04}'
    emp.user = obj
    emp.right = right
    emp.save()


@receiver(post_save, sender=User)
def first_actions(sender, instance, created, **kwargs):
    if created:
        create_initial_access_right(instance)
        create_first_employee(instance)


@receiver(post_save, sender=Shops)
def owner_all_shops(sender, instance, created, **kwargs):
    if created:
        try:
            right = Rights.objects.get(is_owner=True, user=instance.user)
            emp = Employees.objects.get(right=right, user=instance.user)
            shops = Shops.objects.filter(user=instance.user)
            for shop in shops:
                emp.shops.add(shop)
            emp.save()
        except ObjectDoesNotExist:
            pass
