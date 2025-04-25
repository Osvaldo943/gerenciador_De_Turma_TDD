import re 

class Email():
    def __init__(self, value):
        if(not self.is_valid_email(value)):
            raise ValueError("Email inválido")
        
        self._value = value
    
    def is_valid_email(self, value):
        return re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", value) is not None

    def value(self): 
        return str(self._value)