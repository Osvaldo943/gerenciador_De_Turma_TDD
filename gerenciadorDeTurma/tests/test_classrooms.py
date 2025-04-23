import unittest
from enrollment.domain.service.enrollment_service import EnrollmentService
from enrollment.domain.repository.classroom_repository import ClassroomRepository
from enrollment.domain.model.classroom import Classroom
from enrollment.domain.service.notification_service import NotifyStudentService
from enrollment.domain.model.student import Student 
from enrollment.domain.repository.enrollment_repository import EnrollmentRepository
from enrollment.domain.service.payment_note_service import PaymentNoteService
from enrollment.domain.repository.payment_note_repository import PaymentNoteRepository
from enrollment.adapters.driven.event_bus import events 
from enrollment.domain.model.student import Email 
from enrollment.domain.policy.classroom_policy import ClassroomPolicy
from enrollment.adapters.driven.event_bus import event_bus

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
    
    def test_criar_turma(self):
        """"Deve criar turma e adicionar no repositório de turmas quando uma turma for criada"""

        classroomPolicy = ClassroomPolicy    
        enrollmentRepository = EnrollmentRepository()
        classroomRepository = ClassroomRepository()
        classroomPolicy = ClassroomPolicy
        enrollmentService = EnrollmentService(classroomRepository, enrollmentRepository, classroomPolicy)
        
        classroom = Classroom(self.students)

        enrollmentService.save_classroom_in_repository(classroom)
        allClassrooms = classroomRepository.get_classrooms()
        self.assertEqual(len(allClassrooms), 1)


    def test_disparar_evento_turma_criada(self):    
        """Deve disparar o evento turma_criada quando uma turma for criada"""

        classroomPolicy = ClassroomPolicy
        enrollmentRepository = EnrollmentRepository()
        classroomRepository = ClassroomRepository()
        classroomPolicy = ClassroomPolicy
        enrollmentService = EnrollmentService(classroomRepository, enrollmentRepository, classroomPolicy)
        
        classroom = Classroom(self.students)
        
        enrollmentService.save_classroom_in_repository(classroom)
        
        self.assertTrue(self.isClassroomCreated)

    def test_nao_deve_criar_turma_com_menos_de_4_estudantes(self):
        """Não deve criar turma com menos de 4 estudantes"""

        with self.assertRaises(ValueError):
            classroom = Classroom(self.students[:3])

if __name__ == "__main__":
    unittest.main()