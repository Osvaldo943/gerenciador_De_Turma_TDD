import uuid
import re 

class Student(): 
    def __init__(self, name, email: "Email", age):
        self.id = int(str(uuid.uuid4().int)[:8])
        self.name = name
        self.email: Email = email
        self.age = age
        self.isNotified = False

    def notifiedStudent(self):
        self.isNotified = True 
        print(self.name, " notificado")


class Email():
    def __init__(self, value):
        if(self.is_valid_email(value)):
            raise ValueError("Email inválido")
        
        self.value = value
    
    def is_valid_email(self, value):
        return re.match("/^[^\s@]+@[^\s@]+\.[^\s@]+$/", value) is not None

    def value(self): 
        return self.value