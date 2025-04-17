import unittest
from enrollment.enrollment_service import EnrollmentService
from enrollment.classroom_repository import ClassroomRepository
from enrollment.classroom import Classroom
from notification.notification_service import NotifyStudentService
from enrollment.student import Student 
from enrollment.waiting_list_repository import WaitingListRepository
from payment.payment_note_service import PaymentNoteService
from payment.payment_note_repository import PaymentNoteRepository
from event_bus import events
from enrollment.student import Email 
from event_bus import event_bus

class testes(unittest.TestCase):
    def setUp(self): 
        self.students: list[Student] = [
            Student("Joelson dos Santos", Email("joelson@gmail.com"), 24),
            Student("Osvaldo dos Santos", Email("osvaldo@gmail.com"), 24),
            Student("Lemos dos Santos", Email("lemos@gmail.com"), 24),
            Student("Rui dos Santos", Email("rui@gmail.com"), 24),
        ]

        self.isClassroomCreated = False
        self.isStudentNotified = False
        self.isStudentEnrolled = False

        def verify_classroom_event(payload):
            self.isClassroomCreated = True

        def verify_student_notification_event(payload):
            self.isStudentNotified = True
        
        def verify_student_enrollment_event(palyload):
            self.isStudentEnrolled = True

        event_bus.subscribe(events.classRoomCreated, verify_classroom_event)
        event_bus.subscribe(events.studentNotified, verify_student_notification_event)
        event_bus.subscribe(events.studentEnrolled, verify_student_enrollment_event)
    
    def test_notificar_alunos(self):
        """"Deve notificar cada aluno de uma turma quando a turma for criada"""

        waitingListRepository = WaitingListRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, waitingListRepository)
        classroom = Classroom(self.students)
        
        notifyStudentService = NotifyStudentService()

        def notify(self): 
             notifyStudentService.notify(classroom)

        event_bus.subscribe(events.classRoomCreated, notify)

        enrollmentService.create_classroom(classroom)

        allClassrooms: list[Classroom] = classroomRepository.get_classrooms()
        
        self.assertEqual(allClassrooms[0].students[0].isNotified, True)
        self.assertEqual(allClassrooms[0].students[1].isNotified, True)
        self.assertEqual(allClassrooms[0].students[2].isNotified, True)

    def test_disparar_evento_aluno_notificado(self):
        """Deve disparar evento alunos_notificados quando um aluno for notificado"""
        waitingListRepository = WaitingListRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, waitingListRepository)

        classroom = Classroom(self.students)
        notifyStudentService = NotifyStudentService()
        
        def notify_student(self): 
             notifyStudentService.notify(classroom)

        event_bus.subscribe(events.classRoomCreated, notify_student)

        enrollmentService.create_classroom(classroom)

        self.assertTrue(self.isStudentNotified)

if __name__ == "__main__":
    unittest.main()