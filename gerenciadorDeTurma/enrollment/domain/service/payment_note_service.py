from enrollment.domain.repository.payment_note_repository import PaymentNoteRepository
from enrollment.domain.model.classroom import Classroom
from enrollment.domain.model.payment_note import PaymentNote
from enrollment.shared.event_bus import event_bus
from enrollment.shared.event_bus import events

class PaymentNoteService:
    def __init__(self, paymentNoteRepository: "PaymentNoteRepository"):
        self.paymentNoteRepository = paymentNoteRepository
    
    def generate_payment_note(self, classroom: "Classroom", price, dueDate):
        for student in classroom.students:
            newPaymentNote = PaymentNote(classroom.id+student.id, price, dueDate)
            self.paymentNoteRepository.save_payment(newPaymentNote)
            event_bus.publish(events.studentNotified, student)