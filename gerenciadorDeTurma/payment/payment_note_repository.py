from payment.payment_note import PaymentNote

class PaymentNoteRepository():
    def __init__(self):
        self.paymentNotes = []

    def save_payment(self, paymentNote: "PaymentNote"):
        self.paymentNotes.append(paymentNote)

    def get_payment_note(self):
        return self.paymentNotes
