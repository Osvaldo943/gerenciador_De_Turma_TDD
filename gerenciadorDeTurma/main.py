from enrollment.aplication.service.enrollment_service import EnrollmentService
from enrollment.adapters.driven.classroom_repository import ClassroomRepository
from enrollment.domain.policy.classroom_policy import ClassroomPolicy
from enrollment.adapters.driven.enrollment_repository import EnrollmentRepository
from enrollment.adapters.driven.payment_note_repository import PaymentNoteRepository
from enrollment.adapters.driving.cli import CLI
from enrollment.aplication.service.notification_service import NotificationService
from enrollment.aplication.service.payment_note_service import PaymentNoteService
from enrollment.adapters.driven.event_bus import EventBus 
from enrollment.domain.events.events import events
from enrollment.adapters.driven.sql_enrollment_repository import SQLiteEnrollmentRepository
from enrollment.adapters.driven.sql_classroom_repository import SQLiteclassroomRepository
from enrollment.adapters.driven.sql_payment_note_repository import SQLitePaymentNoteReository
from enrollment.adapters.driven.emailSender import EmailSender
 
if __name__ == "__main__":
    print("="*60)
    print(" "*15 + "Sistema de Inscrição ")
    print("="*60) 
     
    sqlLiteEnrollmentRepositoryAdapter = SQLiteEnrollmentRepository()
    sqlLiteClassroomRepositoryAdapter = SQLiteclassroomRepository()
    sqlLitePaymnentNoteRepositoryAdapter = SQLitePaymentNoteReository()
    
    emailSender = EmailSender()
    classroomPolicy = ClassroomPolicy()
    eventBusAdapter = EventBus()
    
    notificationService = NotificationService(emailSender,eventBusAdapter) 
    paymentService = PaymentNoteService(sqlLitePaymnentNoteRepositoryAdapter, eventBusAdapter)
    
    eventBusAdapter.subscribe(events.classRoomCreated, lambda payload:  notificationService.notify(payload))
    eventBusAdapter.subscribe(events.classRoomCreated, lambda payload:  paymentService.generate_payment_note(payload, 5000, "10/12/2025"))
    
    enrollmentService = EnrollmentService(sqlLiteClassroomRepositoryAdapter, classroomPolicy, sqlLiteEnrollmentRepositoryAdapter, eventBusAdapter)
    
    cli = CLI(enrollmentService, paymentService)
    
    cli.run() 
    