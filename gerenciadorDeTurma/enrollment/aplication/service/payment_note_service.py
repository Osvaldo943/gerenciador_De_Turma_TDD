from enrollment.domain.ports.driven.payment_note_repository import IPaymentNoteRepository
from enrollment.domain.model.classroom import Classroom
from enrollment.domain.model.payment_note import PaymentNote
from enrollment.domain.events.events import events
from enrollment.domain.ports.driven.event_bus_publisher import IEventBusPublisher
from typing import List

class PaymentNoteService: 
    def __init__(self, paymentNoteRepository: "IPaymentNoteRepository", eventBus:IEventBusPublisher):
        self.paymentNoteRepository = paymentNoteRepository
        self.eventBus = eventBus
    
    def generate_payment_note(self, classroom: "Classroom", price, dueDate):
        self.price = price
        self.dueDate = dueDate
        
        paymentNotes = []
        for student in classroom.students:
            newPaymentNote = PaymentNote(student.id, price, dueDate)
            self.paymentNoteRepository.save(newPaymentNote)
            paymentNotes.append(newPaymentNote)
            self.eventBus.publish(events.studentNotified, student)
        
        print("\n==> Notificação: Notas de pagamento geradas")
        self.eventBus.publish(events.paymentNoteGenerated, paymentNotes)
        
    def getAllPaymentNote(self)-> List["PaymentNote"]:
        return self.paymentNoteRepository.getAll()