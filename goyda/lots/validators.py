from django.core.exceptions import ValidationError
import re

class Validator:
    
    @staticmethod
    def path(path: str):
        if not path.endswith('/'):
            raise ValidationError('Path must end with "/"')
        
        regex = r'^[a-zA-Z0-9\-._~:/?#\[\]@!$&\'()*+,;=%]*$'
        if re.match(regex, path) is None: 
            raise ValidationError('The path contains invalid characters')