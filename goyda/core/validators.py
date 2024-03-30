from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible
from typing import Optional
import re
import abc


@deconstructible
class CustomValidator(abc.ABC):
    error_message = {
        'typeError': _('an argument of the wrong type was passed'),
        'indexError': _('incorrect argument structure'),
        'valueError': _('the value of the argument is not correct'),
        
        'lettersError': _('this field must contain only letters'),
        'max_lengthError': _('you have exceeded the limit: '),
        'min_lengthError': _('you have not entered enough characters. This field must contain from characters: ')
    }
    
    def __init__(self, change_error_message: Optional[list[str, str] | tuple[str, str]], code: str):
        if change_error_message is not None:
            try:
                for i in change_error_message:
                    self.error_message[i[0]] = _(i[1])
            except TypeError:
                raise TypeError(f"{self.error_message['typeError']} (change_error_message)")
            except IndexError:
                raise IndexError(f"{self.error_message['indexError']} (change_error_message)")

        try:
            self.code = str(code)
        except TypeError:
            raise TypeError(f"{self.error_message['typeError']} (code)")

    @abc.abstractmethod
    def __call__(self, data):
        """Validator Logic"""

@deconstructible
class NameValidator(CustomValidator):
    code = 'invalid'
    
    def __init__(self, min_lenght: int = 2, max_lenght: int = 24,
                 change_error_message: Optional[list[str, str] | tuple[str, str]] = None,
                 code: str = code):
        super().__init__(change_error_message, code)
            
        if not isinstance(min_lenght, int) or min_lenght < 0:
            raise ValueError(f"{self.error_message['valueError']} (min_lenght)")
        if not isinstance(max_lenght, int) or max_lenght < 2 or min_lenght > max_lenght:
            raise ValueError(f"{self.error_message['valueError']} (max_lenght)")
        
        self.min_lenght = min_lenght
        self.max_lenght = max_lenght
        
    def __call__(self, name: str):
        try:
            name = str(name)
        except TypeError:
            raise TypeError(f"{self.error_message['typeError']} (name)")
        
        if not name.isalpha():
            raise ValidationError(self.error_message['lettersError'], code=self.code)
        elif len(name) > self.max_lenght:
            raise ValidationError(self.error_message['max_lengthError'] + str(self.max_lenght), code=self.code)
        elif len(name) < self.min_lenght:
            raise ValidationError(self.error_message['min_lengthError'] + str(self.min_lenght), code=self.code)
        

@deconstructible
class PathValidator(CustomValidator):
    code = 'invalid'
    regex = r'^[a-zA-Z0-9\-._~:/?#\[\]@!$&\'()*+,;=%]*$'
    
    def __init__(self, change_error_message: Optional[list[str, str] | tuple[str, str]] = None,
                 code: str = code, regex: str = regex):
        super().__init__(change_error_message, code)
        try:
            re.compile(regex)
        except re.error:
            raise TypeError(f"{self.error_message['typeError']} (regex)")
        self.regex = regex
        
        
    def __call__(self, path: str):
        try:
            path = str(path)
        except TypeError:
            raise TypeError(f"{self.error_message['typeError']} (path)")
        
        if not path.endswith('/'):
            raise ValidationError(self.error_message['valueError'] + _('The path must end in /'), code=self.code)
        if re.match(self.regex, path) is None: 
            raise ValidationError(self.error_message['valueError'] + _('The path contains invalid characters'), code=self.code)
    
    
    
@deconstructible
class CityValidator(CustomValidator):
    code = 'invalid'
    regex = r"^([a-z\u0080-\u024F]+(?:. |-| |'))*[a-z\u0080-\u024F]*$"
    
    def __init__(self, min_lenght: int = 2, max_lenght: int = 24,
                 change_error_message: Optional[list[str, str] | tuple[str, str]] = None,
                 code: str = code, regex: str = regex):
        super().__init__(change_error_message, code)
        
        try:
            re.compile(regex)
        except re.error:
            raise TypeError(f"{self.error_message['typeError']} (regex)")
        self.regex = regex
        
        if not isinstance(min_lenght, int) or min_lenght < 0:
            raise ValueError(f"{self.error_message['valueError']} (min_lenght)")
        if not isinstance(max_lenght, int) or max_lenght < 2 or min_lenght > max_lenght:
            raise ValueError(f"{self.error_message['valueError']} (max_lenght)")
        
        self.min_lenght = min_lenght
        self.max_lenght = max_lenght
        
    def __call__(self, city: str):
        try:
            city = str(city)
        except TypeError:
            raise TypeError(f"{self.error_message['typeError']} (city)")
        
        if re.match(self.regex, city) is None or " " in city:
            raise ValidationError(self.error_message['valueError'] + _('Enter the correct name of the city (fill in all the spaces with "-", use only lowercase characters)'), code=self.code)
        elif len(city) > self.max_lenght:
            raise ValidationError(self.error_message['max_lengthError'] + str(self.max_lenght), code=self.code)
        elif len(city) < self.min_lenght:
            raise ValidationError(self.error_message['min_lengthError'] + str(self.min_lenght), code=self.code)
    

@deconstructible
class PhoneNumberValidator(CustomValidator):
    code = 'invalid'
    regex = r'^\+\d+$'
    
    def __init__(self, min_lenght: int = 8, max_lenght: int = 19,
                 change_error_message: Optional[list[str, str] | tuple[str, str]] = None,
                 code: str = code, regex: str = regex):
        super().__init__(change_error_message, code)
        
        try:
            re.compile(regex)
        except re.error:
            raise TypeError(f"{self.error_message['typeError']} (regex)")
        self.regex = regex
        
        if not isinstance(min_lenght, int) or min_lenght < 0:
            raise ValueError(f"{self.error_message['valueError']} (min_lenght)")
        if not isinstance(max_lenght, int) or max_lenght < 2 or min_lenght > max_lenght:
            raise ValueError(f"{self.error_message['valueError']} (max_lenght)")
        
        self.min_lenght = min_lenght
        self.max_lenght = max_lenght
        
        
    def __call__(self, phone_number: str):
        try:
            phone_number = str(phone_number)
        except TypeError:
            raise TypeError(f"{self.error_message['typeError']} (phone_number)")
        
        if re.match(self.regex, phone_number):
            raise ValidationError(self.error_message['valueError'] + _('the phone number is uncorrected'), code=self.code)
        elif len(phone_number) > self.max_lenght:
            raise ValidationError(self.error_message['max_lengthError'] + str(self.max_lenght), code=self.code)
        elif len(phone_number) < self.min_lenght:
            raise ValidationError(self.error_message['min_lengthError'] + str(self.min_lenght), code=self.code)
  
    