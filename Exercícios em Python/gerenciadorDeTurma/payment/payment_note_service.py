from payment.payment_note_repository import PaymentNoteRepository
from enrollment.classroom import Classroom
from payment.payment_note import PaymentNote
from event_bus import event_bus
from event_bus import events

class PaymentNoteService:
    def __init__(self, paymentNoteRepository: "PaymentNoteRepository"):
        self.paymentNoteRepository = paymentNoteRepository
    
    def generate_payment_note(self, classroom: "Classroom", price, dueDate):
        for student in classroom.students:
            newPaymentNote = PaymentNote(classroom.id+student.id, price, dueDate)
            self.paymentNoteRepository.save_payment(newPaymentNote)
            event_bus.publish(events.studentNotified, student)