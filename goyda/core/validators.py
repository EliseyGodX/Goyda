from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

class Validator:
    
    @staticmethod
    def path(hint='path'):
        def validator(path):
            if not path.endswith('/'):
                raise ValidationError(
                    _(f'{hint} must end with "/"'),
                    code='invalid')
            regex = r'^[a-zA-Z0-9\-._~:/?#\[\]@!$&\'()*+,;=%]*$'
            if re.match(regex, path) is None: 
                raise ValidationError(
                    _(f'The {hint} contains invalid characters'),
                    code='invalid')
        return validator  
        
    @staticmethod
    def custom_name(hint='name'):
        def validator(data):
            regex = r'^[a-zA-Z0-9\-._~:/?#\[\]@!$&\'()*+,;=%]*$'
            if not data[0].isalpha():
                raise ValidationError(
                    _(f'The {hint} must start with a letter'),
                    code='invalid')
            if re.match(regex, data) is None: 
                raise ValidationError(
                    _(f'The {hint} contains invalid characters'),
                    code='invalid')
            if len(data) < 2:
                raise ValidationError(
                    _(f'The {hint} is too short'),
                    code='min_lenght')
        return validator     
        
    @staticmethod
    def custom_name_onlyAlpha(hint='name'):
        def validator(data):
            first_check = Validator.custom_name(hint)
            first_check(data)
            if not data.isalpha():
                raise ValidationError(
                    _(f'The {hint} contains invalid characters'),
                    code='invalid')
        return validator
        
    @staticmethod
    def city(hint='city'):
        def validator(city):
            regex = r"^([a-z\u0080-\u024F]+(?:. |-| |'))*[a-z\u0080-\u024F]*$"
            if re.match(regex, city) is None   or " " in city   or len(city) == 1: 
                raise ValidationError(
                    _(f'Enter the correct name of the {hint} (fill in all the spaces with "-", use only lowercase characters)'),
                    code='invalid')
        return validator
        
    @staticmethod
    def phone_number(hint='phone number'):
        def validator(number):
            if not number.startswith('+'): 
                raise ValidationError(
                    _(f'The {hint} must start with "+"'),
                    code='invalid')
            elif len(number) < 8:
                raise ValidationError(
                    _(f'The {hint} is too short'),
                    code='min_lenght')
        return validator
        
    @staticmethod
    def age(low_age='The auction is intended for users who are over 18', 
            ower_age='Not a funny joke'):
        def validator(age):
            if age < 18: 
                raise ValidationError(
                    _(low_age),
                    code='min_age')
            elif age > 99:
                raise ValidationError(
                    _(ower_age),
                    code='over_age')
        return validator