from enrollment.domain.model.email import Email
import uuid

class Student(): 
    def __init__(self, name, email: "Email", age):
        self.id = int(str(uuid.uuid4().int)[:8])
        self.name = name
        self.email: Email = email
        self.age = age
        self.isNotified = False

    def mark_as_notified(self):
        self.isNotified = True 
        print(self.name, " notificado")


