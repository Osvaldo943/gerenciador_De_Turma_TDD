from enrollment.domain.model.payment_note import PaymentNote
from typing import List

class PaymentNoteRepository():
    def __init__(self):
        self.paymentNotes: List["PaymentNote"] = []

    def save(self, paymentNote: "PaymentNote"):
        self.paymentNotes.append(paymentNote)

    def getAll(self):
        return list(self.paymentNotes)
