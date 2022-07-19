from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


class Accounts(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(_('Description'), blank=True)

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        db_table = 'accounts'
        verbose_name = 'account'
        verbose_name_plural = 'account'

    def __str__(self):
        return '%s' % self.description

