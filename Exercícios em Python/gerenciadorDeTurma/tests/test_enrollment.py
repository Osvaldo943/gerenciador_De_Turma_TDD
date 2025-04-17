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
    
    def test_deve_inscrever_aluno(self):
        """Deve adicionar aluno na lista de espera quando ele for inscrito"""
        
        student1 = Student("Alfredo de Sousa", "alfredo@gmail.com", 20)

        waitingListRepository = WaitingListRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, waitingListRepository)
        
        enrollmentService.enroll(student1)

        allStudentWaiting = waitingListRepository.get_waiting_students()

        self.assertEqual(len(allStudentWaiting), 1)

    def test_deve_disparar_aluno_inscrito(self):
        """Deve disparar o evento aluno inscrito quando um aluno for inscrito"""
         
        student1 = Student("Alfredo de Sousa", "alfredo@gmail.com", 20)

        waitingListRepository = WaitingListRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, waitingListRepository)
        
        enrollmentService.enroll(student1)

        allStudentWaiting = waitingListRepository.get_waiting_students()

        self.assertEqual(len(allStudentWaiting), 1)
        self.assertTrue(self.isStudentEnrolled)
    
    def test_deve_evitar_duplicacao_de_alunos(self):
        """Deve evitar duplicação de alunos ao ser inscrito"""
         
        student1 = Student("Alfredo de Sousa", "alfredo@gmail.com", 20)

        waitingListRepository = WaitingListRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, waitingListRepository)
        
        enrollmentService.enroll(student1)
        enrollmentService.enroll(student1)
        enrollmentService.enroll(student1)

        allStudentWaiting = waitingListRepository.get_waiting_students()

        self.assertEqual(len(allStudentWaiting), 1)
        self.assertTrue(self.isStudentEnrolled)

    def test_deve_criar_turma_quando_estudante_suficiente(self):
        """Deve criar turma quando a lista de espera de alunos alunos for suficiente"""
        
        student1 = Student("Alfredo de Sousa", Email("alfredo@gmail.com"), 20)
        student2 = Student("Osvaldo de Sousa", Email("osvaldo@gmail.com"), 20)
        student3 = Student("Bislânia de Sousa", Email("bis@gmail.com"), 20)
        student4 = Student("Rosa de Sousa", Email("rosa@gmail.com"), 20)

        waitingListRepository = WaitingListRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, waitingListRepository)
        
        enrollmentService.enroll(student1)
        enrollmentService.enroll(student2)
        enrollmentService.enroll(student3)
        enrollmentService.enroll(student4)

        allClassrooms = classroomRepository.get_classrooms()

        self.assertEqual(len(allClassrooms), 1)

    def test_limpar_a_lista_de_espera_apos_criar_turma(self):
        """Deve limpar a lista de espera apôs criar turma"""
        
        student1 = Student("Alfredo de Sousa", Email("alfredo@gmail.com"), 20)
        student2 = Student("Osvaldo de Sousa", Email("osvaldo@gmail.com"), 20)
        student3 = Student("Bislânia de Sousa", Email("bis@gmail.com"), 20)
        student4 = Student("Rosa de Sousa", Email("rosa@gmail.com"), 20)

        waitingListRepository = WaitingListRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, waitingListRepository)
        
        enrollmentService.enroll(student1)
        enrollmentService.enroll(student2)
        enrollmentService.enroll(student3)

        allStudentWaiting = waitingListRepository.get_waiting_students()
        self.assertEqual(len(allStudentWaiting), 3)

        enrollmentService.enroll(student4)

        allStudentWaiting = waitingListRepository.get_waiting_students()
        self.assertEqual(len(allStudentWaiting), 0)

    def test_nao_deve_criar_turma_quando_estudante_insuficiante(self):
        """Não deve criar turma quando a lista de espera de alunos for insuficiente"""
        
        student1 = Student("Alfredo de Sousa", Email("alfredo@gmail.com"), 20)
        student2 = Student("Osvaldo de Sousa", Email("osvaldo@gmail.com"), 20)
        student3 = Student("Bislânia de Sousa", Email("bis@gmail.com"), 20)

        waitingListRepository = WaitingListRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, waitingListRepository)
        
        enrollmentService.enroll(student1)
        enrollmentService.enroll(student2)
        enrollmentService.enroll(student3)

        allClassrooms = classroomRepository.get_classrooms()

        self.assertEqual(len(allClassrooms), 0)

if __name__ == "__main__":
    unittest.main()