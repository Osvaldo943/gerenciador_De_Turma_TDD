import unittest
from enrollment.enrollment_service import EnrollmentService
from enrollment.classroom_repository import ClassroomRepository
from enrollment.classroom import Classroom
from notification.notification_service import NotifyStudentService
from enrollment.student import Student 
from enrollment.waiting_list_repository import WaitingListRepository
from payment.payment_note_service import PaymentNoteService
from payment.payment_note_repository import PaymentNoteRepository


from event_bus import event_bus

class testes(unittest.TestCase):
    def setUp(self): 
        self.students: list[Student] = [
            Student("Joelson dos Santos", "joelson@gmail.com", 24),
            Student("Osvaldo dos Santos", "osvaldo@gmail.com", 24),
            Student("Lemos dos Santos", "lemos@gmail.com", 24),
            Student("Rui dos Santos", "rui@gmail.com", 24),
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

        event_bus.subscribe("classroomCreated", verify_classroom_event)
        event_bus.subscribe("studentsNotified", verify_student_notification_event)
        event_bus.subscribe("studentEnrolled", verify_student_enrollment_event)
    
    def test_criar_turma(self):
        """"Deve adicionar turma no repositório de turmas quando uma turma for criada"""
    
        waitingListRepository = WaitingListRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, waitingListRepository)
        
        classroom = Classroom(self.students)

        enrollmentService.create_classroom(classroom)
        allClassrooms = classroomRepository.get_classroom()
        self.assertEqual(len(allClassrooms), 1)


    def test_disparar_evento(self):    
        """Deve disparar o evento turma_criada quando uma turma for criada"""

        waitingListRepository = WaitingListRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, waitingListRepository)
        
        classroom = Classroom(self.students)
        
        enrollmentService.create_classroom(classroom)
        
        self.assertTrue(self.isClassroomCreated)

    def test_notificar_alunos(self):
        """"Deve notificar cada aluno de uma turma quando a turma for criada"""

        waitingListRepository = WaitingListRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, waitingListRepository)
        classroom = Classroom(self.students)
        
        notifyStudentService = NotifyStudentService()

        def notify(self): 
             notifyStudentService.notify(classroom)

        event_bus.subscribe("classroomCreated", notify)

        enrollmentService.create_classroom(classroom)

        allClassrooms: list[Classroom] = classroomRepository.get_classroom()
        
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
        
        def notify(self): 
             notifyStudentService.notify(classroom)

        event_bus.subscribe("classroomCreated", notify)

        enrollmentService.create_classroom(classroom)

        self.assertTrue(self.isStudentNotified)

    def test_deve_inscrever_aluno(self):
        """Deve adicionar aluno na lista de espera quando ele for inscrito"""
        
        student1 = Student("Alfredo de Sousa", "alfredo@gmail.com", 20)

        waitingListRepository = WaitingListRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, waitingListRepository)
        
        enrollmentService.enroll(student1)

        allStudentWaiting = waitingListRepository.get_waiting_student()

        self.assertEqual(len(allStudentWaiting), 1)

    def test_deve_disparar_aluno_inscrito(self):
        """Deve disparar o evento aluno inscrito quando um aluno for inscrito"""
         
        student1 = Student("Alfredo de Sousa", "alfredo@gmail.com", 20)

        waitingListRepository = WaitingListRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, waitingListRepository)
        
        enrollmentService.enroll(student1)

        allStudentWaiting = waitingListRepository.get_waiting_student()

        self.assertEqual(len(allStudentWaiting), 1)
        self.assertTrue(self.isStudentEnrolled)
    
    def test_deve_criar_turma_quando_estudante_suficiente(self):
        """Deve criar turma quando a lista de espera de alunos alunos for suficiente"""
        
        student1 = Student("Alfredo de Sousa", "alfredo@gmail.com", 20)
        student2 = Student("Osvaldo de Sousa", "osvaldo@gmail.com", 20)
        student3 = Student("Bislânia de Sousa", "bis@gmail.com", 20)
        student4 = Student("Rosa de Sousa", "rosa@gmail.com", 20)

        waitingListRepository = WaitingListRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, waitingListRepository)
        
        enrollmentService.enroll(student1)
        enrollmentService.enroll(student2)
        enrollmentService.enroll(student3)
        enrollmentService.enroll(student4)

        allClassrooms = classroomRepository.get_classroom()

        self.assertEqual(len(allClassrooms), 1)

    def test_nao_deve_criar_turma_quando_estudante_insuficiante(self):
        """Não deve criar turma quando a lista de espera de alunos for insuficiente"""
        
        student1 = Student("Alfredo de Sousa", "alfredo@gmail.com", 20)
        student2 = Student("Osvaldo de Sousa", "osvaldo@gmail.com", 20)
        student3 = Student("Bislânia de Sousa", "bis@gmail.com", 20)

        waitingListRepository = WaitingListRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, waitingListRepository)
        
        enrollmentService.enroll(student1)
        enrollmentService.enroll(student2)
        enrollmentService.enroll(student3)

        allClassrooms = classroomRepository.get_classroom()

        self.assertEqual(len(allClassrooms), 0)

    def test_nota_de_pagemento(self):
        """Deve gerar nota de pagamentos para alunos de uma turma"""
        waitingListRepository = WaitingListRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, waitingListRepository)
        
        classroom = Classroom(self.students)

        enrollmentService.create_classroom(classroom)
        allClassrooms = classroomRepository.get_classroom()

        paymentNoteRepository = PaymentNoteRepository()
        paymentService = PaymentNoteService(paymentNoteRepository)
        paymentService.generate_payment_note(classroom, 10000, "30/05/2025")

        allPaymentNotes = paymentNoteRepository.get_payment_note()

        self.assertEqual(len(allPaymentNotes), 4)


if __name__ == "__main__":
    unittest.main()