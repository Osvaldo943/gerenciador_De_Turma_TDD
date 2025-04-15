import uuid

class Student(): 
    def __init__(self, name, email, age):
        self.id = int(str(uuid.uuid4().int)[:8])
        self.name = name
        self.email = email
        self.age = age
        self.isNotified = False
        