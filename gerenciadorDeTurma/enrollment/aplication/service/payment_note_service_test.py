import unittest
from enrollment.aplication.service.enrollment_service import EnrollmentService
from enrollment.adapters.driven.classroom_repository import ClassroomRepository
from enrollment.domain.model.classroom import Classroom
from enrollment.domain.model.student import Student 
from enrollment.adapters.driven.enrollment_repository import EnrollmentRepository
from enrollment.domain.events.events import events
from enrollment.domain.model.student import Email 
from enrollment.adapters.driven.event_bus import EventBus
from enrollment.domain.policy.classroom_policy import ClassroomPolicy
from enrollment.aplication.service.notification_service import NotificationService
from enrollment.aplication.service.payment_note_service import PaymentNoteService
from enrollment.adapters.driven.payment_note_repository import PaymentNoteRepository

class testes(unittest.TestCase):
    def setUp(self): 
        self.students: list[Student] = [
            Student("Joelson dos Santos", Email("joelson@gmail.com"), 24),
            Student("Osvaldo dos Santos", Email("osvaldo@gmail.com"), 24),
        ]

        self.isClassroomCreated = False
        self.isStudentNotified = False
        self.isStudentEnrolled = False
        self.isPaymentNotesGenerated = False
        self.event_bus = EventBus()

        def verify_payment_note_event(payload):
            self.isPaymentNotesGenerated = True

        self.event_bus.subscribe(events.paymentNoteGenerated, verify_payment_note_event)
        
    def test_nota_de_pagemento(self):
        """Deve gerar nota de pagamentos para alunos de uma turma quando a turma for criada"""
        classroomPolicy = ClassroomPolicy()
        enrollmentRepository = EnrollmentRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, classroomPolicy, enrollmentRepository, self.event_bus)
        
        classroom = Classroom(self.students)

        enrollmentService.save_classroom_in_repository(classroom)
        allClassrooms = classroomRepository.getAll()

        paymentNoteRepository = PaymentNoteRepository()
        paymentService = PaymentNoteService(paymentNoteRepository, self.event_bus)
        paymentService.generate_payment_note(classroom, 5000, "10/12/2025")

        allPaymentNotes = paymentNoteRepository.getAll()

        self.assertEqual(len(allPaymentNotes), 2)
        self.assertEqual(allPaymentNotes[0].price, 5000)
        self.assertEqual(allPaymentNotes[0].dueDate, "10/12/2025")
        
    def test_deve_disparar_evento_nota_de_pagamento_gerado(self):
        """Deve deve disparar notas de pagamentos geradas sempre após a criação de  uma turma"""
        
        classroomPolicy = ClassroomPolicy()
        enrollmentRepository = EnrollmentRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, classroomPolicy, enrollmentRepository, self.event_bus)
        
        classroom = Classroom(self.students)
        enrollmentService.save_classroom_in_repository(classroom)

        
        paymentNoteRepository = PaymentNoteRepository()
        paymentService = PaymentNoteService(paymentNoteRepository, self.event_bus)
        paymentService.generate_payment_note(classroom, 5000, "10/12/2025")

        self.assertTrue(self.isPaymentNotesGenerated)        
        
