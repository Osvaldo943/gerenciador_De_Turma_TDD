from enrollment.aplication.service.enrollment_service import EnrollmentService
from enrollment.adapters.driven.classroom_repository import ClassroomRepository
from enrollment.adapters.driven.enrollment_repository import EnrollmentRepository
from enrollment.adapters.driven.payment_note_repository import PaymentNoteRepository
from enrollment.adapters.driving.cli import CLI
from enrollment.aplication.service.notification_service import NotificationService
from enrollment.aplication.service.payment_note_service import PaymentNoteService
from enrollment.adapters.driven.event_bus import EventBus
from enrollment.domain.events.events import events
from enrollment.adapters.driven.sql_enrollment_repository import SQLiteEnrollmentRepository

if __name__ == "__main__":
    print("=====================")
    print("Sistema de Inscrição ")
    print("=====================")
    
    inMemoryClassroomRepositoryAdapter = ClassroomRepository()
    inMemoryEnrollmentRepositoryAdapter = EnrollmentRepository()
    inMemoryPaymentRepositoryAdapter = PaymentNoteRepository()
    
    sqlLiteEnrollmentRepositoryAdapter = SQLiteEnrollmentRepository()
    
    eventBusAdapter = EventBus()
    notificationService = NotificationService(eventBusAdapter)
    paymentService = PaymentNoteService(inMemoryPaymentRepositoryAdapter, eventBusAdapter)
    
    eventBusAdapter.subscribe(events.classRoomCreated, lambda payload:  notificationService.notify(payload))
    eventBusAdapter.subscribe(events.classRoomCreated, lambda payload:  paymentService.generate_payment_note(payload))
    
    enrollmentService = EnrollmentService(inMemoryClassroomRepositoryAdapter, sqlLiteEnrollmentRepositoryAdapter, eventBusAdapter)
    
    cli = CLI(enrollmentService)
    
    cli.run() 
    