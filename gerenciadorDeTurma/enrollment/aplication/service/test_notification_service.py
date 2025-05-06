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
 
class testes(unittest.TestCase):
    def setUp(self): 
        self.students: list[Student] = [
            Student("Joelson dos Santos", Email("joelson@gmail.com"), 24),
            Student("Osvaldo dos Santos", Email("osvaldo@gmail.com"), 24),
        ]

        self.isClassroomCreated = False
        self.isStudentNotified = False
        self.isStudentEnrolled = False
        self.event_bus = EventBus()

        def verify_classroom_event(payload):
            self.isClassroomCreated = True

        def verify_student_notification_event(payload):
            self.isStudentNotified = True
        
        def verify_student_enrollment_event(palyload):
            self.isStudentEnrolled = True

        self.event_bus.subscribe(events.classRoomCreated, verify_classroom_event)
        self.event_bus.subscribe(events.studentNotified, verify_student_notification_event)
        self.event_bus.subscribe(events.studentEnrolled, verify_student_enrollment_event)
        
    def test_notificar_alunos(self):
        """"Deve notificar cada aluno de uma turma quando a turma for criada"""
        classroomPolicy = ClassroomPolicy()
        enrollmentRepository = EnrollmentRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, classroomPolicy, enrollmentRepository, self.event_bus)
        classroom = Classroom(self.students)
        
        notifyStudentService = NotificationService(self.event_bus)

        def notify(self): 
             notifyStudentService.notify(classroom)

        self.event_bus.subscribe(events.classRoomCreated, notify)

        enrollmentService.save_classroom_in_repository(classroom)
        
        self.assertEqual(classroom.students[0].isNotified, True)
        self.assertEqual(classroom.students[1].isNotified, True)
        
    def test_disparar_evento_aluno_notificado(self):
        """Deve disparar evento alunos_notificados quando um aluno for notificado"""
        classroomPolicy = ClassroomPolicy()
        enrollmentRepository = EnrollmentRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, classroomPolicy, enrollmentRepository, self.event_bus)
        
        classroom = Classroom(self.students)
        notifyStudentService = NotificationService(self.event_bus)
        
        def notify_student(self): 
            notifyStudentService.notify(classroom)

        self.event_bus.subscribe(events.classRoomCreated, notify_student)

        enrollmentService.save_classroom_in_repository(classroom)

        self.assertTrue(self.isStudentNotified)

    