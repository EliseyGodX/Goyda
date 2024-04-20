import uuid

from core.validators import CityValidator, NameValidator, PhoneNumberValidator
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    
    ID = models.UUIDField(primary_key=True, db_index=True, default=uuid.uuid4)
    first_name = models.CharField(_("first name"), max_length=48, validators=[NameValidator()])
    last_name = models.CharField(_("last name"), max_length=48, validators=[NameValidator()])
    email = models.EmailField(_("email address"))
    
    city = models.CharField(_("the user's city"), db_index=True, max_length=48, validators=[CityValidator()])
    age = models.PositiveSmallIntegerField(_("user's age"), validators=[MaxValueValidator(100)])
    purchases = models.PositiveSmallIntegerField(_("purchases made by the user"), default=0)
    sales = models.PositiveSmallIntegerField(_("sales made by the user"), default=0)
    balance = models.IntegerField(_("user's balance"), default=0)
    about = models.TextField(_("about the user"), blank=True)
    avatar = models.ImageField(_("user's avatar"), upload_to='avatars', default='avatars/default.jpg')
    phone = models.CharField(_("the user's phone number"), validators=[PhoneNumberValidator()], blank=True, max_length=19)
    
    active_lots = models.ManyToManyField('lots.Lots', related_name='active_lots', blank=True)
    archive_lots = models.ManyToManyField('lots.ArchiveLots', related_name='archive_lots', blank=True)
    active_purchases = models.ManyToManyField('lots.Lots', related_name='active_purchases', blank=True)
    active_sell = models.ManyToManyField('lots.Lots', related_name='active_sell', blank=True)
    completed_purchases = models.ManyToManyField('lots.ArchiveLots', related_name='complete_purchases', blank=True)
    completed_sell = models.ManyToManyField('lots.ArchiveLots', related_name='complete_sell', blank=True)
    
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ("-date_joined",)