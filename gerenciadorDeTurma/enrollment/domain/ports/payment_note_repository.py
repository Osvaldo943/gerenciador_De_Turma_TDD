from abc import ABC, abstractmethod
from enrollment.domain.model.payment_note import PaymentNote

class IPaymentNoteRepository(ABC):
    
    @abstractmethod
    def save(self, paymentNote: PaymentNote):
        pass
    
    @abstractmethod
    def getAll(self):
        pass