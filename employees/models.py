from django.db import models
from django.contrib.auth.models import User
from shops.models import Shops
from crum import get_current_user
from django.utils.translation import gettext as _
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from django.utils.translation import gettext as _


STATUS = [
    1, _('Owner'),
    2, _('Administrator'),
    3, _('Manager'),
    4, _('Cashier'),
]


class Employees(models.Model):
    def limit_choices_to_current_user():
        user = get_current_user()
        return {'user': user}

    name = models.CharField(_('Employee Name'), max_length=50, unique=True)
    email = models.EmailField(_('Email'))
    telephone = models.CharField(_('Telephone'), max_length=50, blank=True)
    pin = models.CharField(_('Cashier PIN'), max_length=6)
    shops = models.ManyToManyField(
        Shops,
        limit_choices_to=limit_choices_to_current_user,
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    panels = [
        MultiFieldPanel([FieldPanel('name'), FieldPanel('email'), FieldPanel('telephone')],
                        heading=_('Name, Email and Telephone')),
        FieldPanel('pin'),
        FieldPanel('shops'),
    ]

    class Meta:
        db_table = 'employees'
        verbose_name = 'employee'
        verbose_name_plural = 'employees'

    def __str__(self):
        return '%s' % self.name

    def save(self):
        self.user = get_current_user()
        return super(Employees, self).save()
