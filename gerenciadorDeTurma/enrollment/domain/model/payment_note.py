import uuid

class PaymentNote():
    def __init__(self, idStudent, price, dueDate):
        self.id = int(str(uuid.uuid4().int)[:8])
        self.idStudent = idStudent
        self.price = price
        self.dueDate = dueDate