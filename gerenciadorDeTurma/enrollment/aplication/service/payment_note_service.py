from enrollment.domain.ports.driven.payment_note_repository import IPaymentNoteRepository
from enrollment.domain.model.classroom import Classroom
from enrollment.domain.model.payment_note import PaymentNote
from enrollment.domain.events.events import events
from enrollment.domain.ports.driven.event_bus_publisher import IEventBusPublisher

class PaymentNoteService:
    def __init__(self, paymentNoteRepository: "IPaymentNoteRepository", eventBus:IEventBusPublisher):
        self.paymentNoteRepository = paymentNoteRepository
        self.eventBus = eventBus
    
    def generate_payment_note(self, classroom: "Classroom"):
        price = 5000
        dueDate = "10/12/2025"
        
        print("\n=======================")
        print("=  Notas de pagamentos  =")
        print("=======================\n")
        
        for student in classroom.students:
            newPaymentNote = PaymentNote(classroom.id+student.id, price, dueDate)
            self.paymentNoteRepository.save(newPaymentNote)
            self.eventBus.publish(events.studentNotified, student)
            print(newPaymentNote.id, " -> Nota de pagamento gerada")