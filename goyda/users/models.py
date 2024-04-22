from uuid_extensions import uuid7

from core.validators import NameValidator, PhoneNumberValidator
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    
    ID = models.UUIDField(primary_key=True, default=uuid7())
    first_name = models.CharField(_("First name"), max_length=48, validators=[NameValidator(only_letters=True)])
    last_name = models.CharField(_("Last name"), max_length=48, validators=[NameValidator(only_letters=True)])
    email = models.EmailField(_("Email address"))
    
    avatar = models.ImageField(_("Avatar"), upload_to='avatars', default='avatars/default.jpg')
    city = models.ForeignKey('core.City', on_delete=models.PROTECT, db_index=True,
                             related_name='cities', verbose_name=_("City"))
    age = models.PositiveSmallIntegerField(_("Age"), validators=[MaxValueValidator(100)])
    balance = models.PositiveBigIntegerField(_("Balance"), default=0)
    about = models.TextField(_("About"), null=True, blank=True)
    phone = models.CharField(_("Phone number"), validators=[PhoneNumberValidator()], 
                             blank=True, null=True, max_length=19)
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table_comment = (
            '''Contains information about the user"'''
            )
        
    def __str__(self):
        return self.username