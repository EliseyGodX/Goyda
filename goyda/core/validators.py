import abc
import re
from typing import Optional

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class CustomValidator(abc.ABC):
    error_message = {
        'typeError': _('an argument of the wrong type was passed ({})'),
        'indexError': _('incorrect argument structure ({})'),
        'valueError': _('the value of the argument is not correct ({})'),
        
        'lettersError': _('this field must contain only letters'),
        'firstLetterError': _('The name must begin with the letter'),
        'max_lengthError': _('you have exceeded the limit: {}'),
        'min_lengthError': _('you have not entered enough characters. This field must contain from characters: {}')
    }
    
    def __init__(self, change_error_message: Optional[list[tuple]], code: str):
        if change_error_message is not None:
            try:
                for i in change_error_message:
                    self.error_message[i[0]] = _(i[1])
            except TypeError:
                raise TypeError(self.error_message['typeError'].format('change_error_message'))
            except IndexError:
                raise IndexError(self.error_message['indexError'].format('change_error_message'))
        try:
            self.code = str(code)
        except TypeError:
            raise TypeError(self.error_message['typeError'].format('code'))

    def len_validators_in_init(self, min_lenght: int, max_lenght: Optional[int]):
        if not isinstance(min_lenght, int) or min_lenght < 0:
            raise ValueError(self.error_message['typeError'].format('min_lenght'))
        if max_lenght is not None:
            if not isinstance(max_lenght, int) or max_lenght < 2 or min_lenght > max_lenght:
                raise ValueError(self.error_message['typeError'].format('max_lenght'))
        
    def len_validators_in_call(self, parameter):
        if len(parameter) > self.max_lenght:
            raise ValidationError(self.error_message['max_lengthError'].format(self.max_lenght), code=self.code)
        elif len(parameter) < self.min_lenght:
            raise ValidationError(self.error_message['min_lengthError'].format(self.min_lenght), code=self.code)
        
    @abc.abstractmethod
    def __call__(self, data):
        """Validator Logic"""
        
        
@deconstructible
class NameValidator(CustomValidator):
    code = 'invalid'
    
    def __init__(self, min_lenght: int = 2, max_lenght: Optional[int] = None,
                 change_error_message:  Optional[list[tuple]] = None,
                 code: str = code, only_letters: bool = True):
        super().__init__(change_error_message, code)
        self.len_validators_in_init(min_lenght, max_lenght)
        self.min_lenght = min_lenght
        self.max_lenght = max_lenght
        self.only_letters = only_letters
        
    def __call__(self, name: str):
        try:
            name = str(name)
        except TypeError:
            raise TypeError(self.error_message['typeError'].format('name'))
        
        if self.only_letters == True and not name.isalpha():
            raise ValidationError(self.error_message['lettersError'], code=self.code)
        elif self.only_letters == False and not name[0].isalpha():
            raise ValidationError(self.error_message['firstLetterError'], code=self.code)
        self.len_validators_in_call(name)      
    

@deconstructible
class PhoneNumberValidator(CustomValidator):
    code = 'invalid'
    regex = r'\+[0-9]+'
    
    def __init__(self, min_lenght: int = 8, max_lenght: Optional[int] = None,
                 change_error_message:  Optional[list[tuple]] = None,
                 code: str = code, regex: str = regex):
        super().__init__(change_error_message, code)
        try:
            re.compile(regex)
        except re.error:
            raise TypeError(self.error_message['typeError'].format('regex'))
        self.regex = regex
        self.len_validators_in_init(min_lenght, max_lenght)
        self.min_lenght = min_lenght
        self.max_lenght = max_lenght
        
    def __call__(self, phone_number: str):
        try:
            phone_number = str(phone_number)
        except TypeError:
            raise TypeError(self.error_message['typeError'].format('phone_number'))
        
        if re.match(self.regex, phone_number) is None:
            raise ValidationError(self.error_message['valueError'].format(_('the phone number is uncorrected')), code=self.code)
        self.len_validators_in_call(phone_number)
  
    