import unittest
from main import EnrollmentService
from main import Repository
from main import Classroom
from main import NotifyStudentService
from main import Student 
from main import WaitingListRepository

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

        def verify_classroom(payload):
            self.isClassroomCreated = True

        def verify_student_notification(payload):
            self.isStudentNotified = True

        event_bus.subscribe("classroomCreated", verify_classroom)
        event_bus.subscribe("studentsNotified", verify_student_notification)
    
    def test_criar_turma(self):
        """"Deve adicionar turma no repositório de turmas quando uma turma for criada"""
    
        waitingListRepository = WaitingListRepository()
        repository = Repository()
        enrollmentService = EnrollmentService(repository, waitingListRepository)
        
        classroom = Classroom(self.students)

        enrollmentService.create_classroom(classroom)
        allClassrooms = repository.get_classroom()
        self.assertEqual(len(allClassrooms), 1)


    def test_disparar_evento(self):    
        """Deve disparar o evento turma_criada quando uma turma for criada"""

        waitingListRepository = WaitingListRepository()
        repository = Repository()
        enrollmentService = EnrollmentService(repository, waitingListRepository)
        
        classroom = Classroom(self.students)
        
        enrollmentService.create_classroom(classroom)
        
        self.assertTrue(self.isClassroomCreated)

    def test_notificar_alunos(self):
        """"Deve notificar cada aluno de uma turma quando a turma for criada"""

        waitingListRepository = WaitingListRepository()
        repository = Repository()
        enrollmentService = EnrollmentService(repository, waitingListRepository)
        classroom = Classroom(self.students)
        
        notifyStudentService = NotifyStudentService()

        def notify(self): 
             notifyStudentService.notify(classroom)

        event_bus.subscribe("classroomCreated", notify)

        enrollmentService.create_classroom(classroom)

        allClassrooms: list[Classroom] = repository.get_classroom()
        
        self.assertEqual(allClassrooms[0].students[0].isNotified, True)
        self.assertEqual(allClassrooms[0].students[1].isNotified, True)
        self.assertEqual(allClassrooms[0].students[2].isNotified, True)

    def test_disparar_evento_aluno_notificado(self):
        """Deve disparar evento alunos_notificados quando um aluno for notificado"""
        waitingListRepository = WaitingListRepository()
        repository = Repository()
        enrollmentService = EnrollmentService(repository, waitingListRepository)

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
        repository = Repository()
        enrollmentService = EnrollmentService(repository, waitingListRepository)
        
        enrollmentService.enroll(student1)

        allStudentWaiting = waitingListRepository.get_student()

        self.assertEqual(len(allStudentWaiting), 1)
    
    def test_deve_criar_turma_estudante_suficiente(self):
        """Deve criar turma quando a lista de espera tiver alunos suficiente"""
        
        student1 = Student("Alfredo de Sousa", "alfredo@gmail.com", 20)
        student2 = Student("Osvaldo de Sousa", "osvaldo@gmail.com", 20)
        student3 = Student("Bislânia de Sousa", "bis@gmail.com", 20)
        student4 = Student("Rosa de Sousa", "rosa@gmail.com", 20)

        waitingListRepository = WaitingListRepository()
        repository = Repository()
        enrollmentService = EnrollmentService(repository, waitingListRepository)
        
        enrollmentService.enroll(student1)
        enrollmentService.enroll(student2)
        enrollmentService.enroll(student3)
        enrollmentService.enroll(student4)

        allClassrooms = repository.get_classroom()

        self.assertEqual(len(allClassrooms), 1)


if __name__ == "__main__":
    unittest.main()