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
    
    def test_deve_inscrever_aluno(self):
        """Deve adicionar aluno na lista de inscrição quando ele for inscrito"""
        
        student1 = Student("Alfredo de Sousa", "alfredo@gmail.com", 20)

        classroomPolicy = ClassroomPolicy()
        enrollmentRepository = EnrollmentRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, classroomPolicy, enrollmentRepository, self.event_bus)
        
        enrollmentService.enroll(student1.name, student1.email, student1.age)

        enrolledStudents = enrollmentRepository.getAll()

        self.assertEqual(len(enrolledStudents), 1)
        
        
    def test_deve_disparar_aluno_inscrito(self):
        """Deve disparar o evento aluno inscrito quando um aluno for inscrito"""
         
        student1 = Student("Alfredo de Sousa", "alfredo@gmail.com", 20)

        classroomPolicy = ClassroomPolicy()
        enrollmentRepository = EnrollmentRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, classroomPolicy, enrollmentRepository, self.event_bus)
        
        enrollmentService.enroll(student1.name, student1.email, student1.age)

        enrolledStudents = enrollmentRepository.getAll()

        self.assertEqual(len(enrolledStudents), 1)
        self.assertTrue(self.isStudentEnrolled)
        
    def test_deve_evitar_duplicacao_de_alunos(self):
        """Deve evitar duplicação de alunos ao ser inscrito"""
         
        student1 = Student("Alfredo de Sousa", "alfredo@gmail.com", 20)

        classroomPolicy = ClassroomPolicy()
        enrollmentRepository = EnrollmentRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, classroomPolicy, enrollmentRepository, self.event_bus)
        
        enrollmentService.enroll(student1.name, student1.email, student1.age)
        enrollmentService.enroll(student1.name, student1.email, student1.age)
        enrollmentService.enroll(student1.name, student1.email, student1.age)
        
        enrolledStudents = enrollmentRepository.getAll()

        self.assertEqual(len(enrolledStudents), 1)

    def test_deve_criar_turma_quando_existir_2_alunos_nao_registrados(self):
        """Deve criar turma quando haver 2 alunos não registrado"""
        
        student1 = Student("Alfredo de Sousa", Email("alfredo@gmail.com"), 20)
        student2 = Student("Osvaldo de Sousa", Email("osvaldo@gmail.com"), 20)
        student3 = Student("Osvaldo de Oliveira", Email("os@gmail.com"), 20)

        classroomPolicy = ClassroomPolicy()
        enrollmentRepository = EnrollmentRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, classroomPolicy, enrollmentRepository, self.event_bus)
        
        enrollmentService.enroll(student1.name, student1.email, student1.age)
        enrollmentService.enroll(student2.name, student2.email, student2.age)
        enrollmentService.enroll(student3.name, student3.email, student3.age)

        allClassrooms = classroomRepository.getAll()

        self.assertEqual(len(allClassrooms), 1)
        
    def test_nao_deve_criar_turma_quando_estudante_insuficiante(self):
        """Não deve criar turma quando a lista de espera de alunos for insuficiente"""
        
        student1 = Student("Alfredo de Sousa", Email("alfredo@gmail.com"), 20)

        classroomPolicy = ClassroomPolicy()
        enrollmentRepository = EnrollmentRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, classroomPolicy, enrollmentRepository, self.event_bus)
        
        enrollmentService.enroll(student1.name, student1.email, student1.age)

        allClassrooms = classroomRepository.getAll()

        self.assertEqual(len(allClassrooms), 0)

if __name__ == "__main__":
    unittest.main()