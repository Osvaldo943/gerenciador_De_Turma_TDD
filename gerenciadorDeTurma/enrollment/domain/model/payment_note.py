import uuid

class PaymentNote():
    def __init__(self, idStudent, price: "Price", dueDate):
        self.id = int(str(uuid.uuid4().int)[:8])
        self.idStudent = idStudent
        self.price = price
        self.dueDate = dueDate
        
 
class Price:
    def __init__(self, value: int) -> None:
        if self.is_valid_price(value):
            raise ValueError("Preço não deve ser negativo")
        
        self.value = value
        
    def is_valid_price(value: int) -> bool: 
        return value > 0