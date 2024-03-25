from django.core.exceptions import ValidationError
import re

class Validator:
    
    @staticmethod
    def path(path, hint='path'):
        if not path.endswith('/'):
            raise ValidationError(f'{hint} must end with "/"')
        
        regex = r'^[a-zA-Z0-9\-._~:/?#\[\]@!$&\'()*+,;=%]*$'
        if re.match(regex, path) is None: 
            raise ValidationError(f'The {hint} contains invalid characters')
        
    @staticmethod
    def custom_name(text, hint='name'):
        regex = r'^[a-zA-Z0-9\-._~:/?#\[\]@!$&\'()*+,;=%]*$'
        if not text[0].isalpha():
            raise ValidationError(f'The {hint} must start with a letter')
        if re.match(regex, text) is None: 
            raise ValidationError(f'The {hint} contains invalid characters')
        if len(text) < 3:
            raise ValidationError(f'The {hint} is too short')
        
    @staticmethod
    def custom_name_onlyAlpha(text, hint='name'):
        Validator.custom_name(text, hint)
        if not text.isalpha():
            raise ValidationError(f'The {hint} is too short')
        
    @staticmethod
    def city(city, hint='city'):
        regex = r"^([a-z\u0080-\u024F]+(?:. |-| |'))*[a-z\u0080-\u024F]*$"
        if re.match(regex, city) is None   or " " in city   or len(city) == 1: 
            raise ValidationError(f'Enter the correct name of the {hint} (fill in all the spaces with "-", use only lowercase characters)')
        
    @staticmethod
    def phone_number(number, hint='phone number'):
        if not number.startswith('+'): 
            raise ValidationError(f'The {hint} must start with "+"')
        elif len(number) < 8:
            raise ValidationError(f'The {hint} is too short')
        
    @staticmethod
    def age(age, hint='The auction is intended for users who are over 18'):
        if age < 18: 
            raise ValidationError(hint)
        elif age > 99:
            raise ValidationError('Not a funny joke')
        
    @staticmethod
    def int_(number, hint='Not a funny joke'):
        forbidden = [228, 1488]
        if number in forbidden:
            raise ValidationError(hint)