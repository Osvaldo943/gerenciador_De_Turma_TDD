from enrollment.domain.model.payment_note import PaymentNote
from typing import List

class PaymentNoteRepository():
    def __init__(self):
        self.paymentNotes: List["PaymentNote"] = []

    def save_payment(self, paymentNote: "PaymentNote"):
        self.paymentNotes.append(paymentNote)

    def get_payment_note(self):
        return list(self.paymentNotes)
