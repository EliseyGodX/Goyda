from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from lots.validators import Validator

class User(AbstractUser):
    
    first_name = models.CharField(_("first name"), max_length=48, validators=[Validator.custom_name_onlyAlpha('first name')])
    last_name = models.CharField(_("last name"), max_length=48, validators=[Validator.custom_name_onlyAlpha('last name')])
    email = models.EmailField(_("email address"))
    
    city = models.CharField(_("the user's city"), max_length=48, validators=[Validator.city])
    age = models.PositiveSmallIntegerField(_("user's age"), validators=[Validator.age])
    purchases = models.PositiveSmallIntegerField(_("purchases made by the user"), default=0)
    sales = models.PositiveSmallIntegerField(_("sales made by the user"), default=0)
    balance = models.IntegerField(_("user's balance"), default=0)
    about = models.TextField(_("about the user"), blank=True)
    avatar = models.ImageField(_("user's avatar"), upload_to='avatars', default='avatars/default.jpg')
    phone = models.CharField(_("the user's phone number"), validators=[Validator.phone_number], blank=True, max_length=19)