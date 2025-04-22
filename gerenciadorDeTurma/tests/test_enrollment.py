import unittest
from enrollment.domain.service.enrollment_service import EnrollmentService
from enrollment.domain.repository.classroom_repository import ClassroomRepository
from enrollment.domain.model.classroom import Classroom
from enrollment.domain.service.notification_service import NotifyStudentService
from enrollment.domain.model.student import Student 
from enrollment.domain.repository.enrollment_repository import EnrollmentRepository
from enrollment.domain.service.payment_note_service import PaymentNoteService
from enrollment.domain.repository.payment_note_repository import PaymentNoteRepository
from enrollment.shared.event_bus import events
from enrollment.domain.model.student import Email 
from enrollment.domain.policy.classroom_policy import ClassroomPolicy
from enrollment.shared.event_bus import event_bus

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
        """Deve adicionar aluno na lista de inscrição quando ele for inscrito"""
        
        student1 = Student("Alfredo de Sousa", "alfredo@gmail.com", 20)

        classroomPolicy = ClassroomPolicy
        enrollmentRepository = EnrollmentRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, enrollmentRepository, classroomPolicy)
        
        enrollmentService.enroll(student1)

        enrolledStudents = enrollmentRepository.get_enrolled_students()

        self.assertEqual(len(enrolledStudents), 1)

    def test_deve_disparar_aluno_inscrito(self):
        """Deve disparar o evento aluno inscrito quando um aluno for inscrito"""
         
        student1 = Student("Alfredo de Sousa", "alfredo@gmail.com", 20)

        classroomPolicy = ClassroomPolicy
        enrollmentRepository = EnrollmentRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, enrollmentRepository, classroomPolicy)
        
        enrollmentService.enroll(student1)

        enrolledStudents = enrollmentRepository.get_enrolled_students()

        self.assertEqual(len(enrolledStudents), 1)
        self.assertTrue(self.isStudentEnrolled)
    
    def test_deve_evitar_duplicacao_de_alunos(self):
        """Deve evitar duplicação de alunos ao ser inscrito"""
         
        student1 = Student("Alfredo de Sousa", "alfredo@gmail.com", 20)

        classroomPolicy = ClassroomPolicy
        enrollmentRepository = EnrollmentRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, enrollmentRepository, classroomPolicy)
        
        enrollmentService.enroll(student1)
        enrollmentService.enroll(student1)
        enrollmentService.enroll(student1)

        enrolledStudents = enrollmentRepository.get_enrolled_students()

        self.assertEqual(len(enrolledStudents), 1)
        self.assertTrue(self.isStudentEnrolled)

    def test_deve_criar_turma_quando_estudante_suficiente(self):
        """Deve criar turma quando a lista de inscrição de alunos alunos for suficiente"""
        
        student1 = Student("Alfredo de Sousa", Email("alfredo@gmail.com"), 20)
        student2 = Student("Osvaldo de Sousa", Email("osvaldo@gmail.com"), 20)
        student3 = Student("Bislânia de Sousa", Email("bis@gmail.com"), 20)
        student4 = Student("Rosa de Sousa", Email("rosa@gmail.com"), 20)

        classroomPolicy = ClassroomPolicy
        enrollmentRepository = EnrollmentRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, enrollmentRepository, classroomPolicy)
        
        enrollmentService.enroll(student1)
        enrollmentService.enroll(student2)
        enrollmentService.enroll(student3)
        enrollmentService.enroll(student4)

        allClassrooms = classroomRepository.get_classrooms()

        self.assertEqual(len(allClassrooms), 1)

    def test_limpar_o_repositório_de_inscrições_apos_criar_turma(self):
        """Deve limpar a lista de inscrição apôs criar turma"""
        
        student1 = Student("Alfredo de Sousa", Email("alfredo@gmail.com"), 20)
        student2 = Student("Osvaldo de Sousa", Email("osvaldo@gmail.com"), 20)
        student3 = Student("Bislânia de Sousa", Email("bis@gmail.com"), 20)
        student4 = Student("Rosa de Sousa", Email("rosa@gmail.com"), 20)

        classroomPolicy = ClassroomPolicy
        enrollmentRepository = EnrollmentRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, enrollmentRepository, classroomPolicy)
        
        enrollmentService.enroll(student1)
        enrollmentService.enroll(student2)
        enrollmentService.enroll(student3)

        enrolledStudents = enrollmentRepository.get_enrolled_students()
        self.assertEqual(len(enrolledStudents), 3)

        enrollmentService.enroll(student4)

        enrolledStudents = enrollmentRepository.get_enrolled_students()
        self.assertEqual(len(enrolledStudents), 0)

    def test_nao_deve_criar_turma_quando_estudante_insuficiante(self):
        """Não deve criar turma quando a lista de inscrições de alunos for insuficiente"""
        
        student1 = Student("Alfredo de Sousa", Email("alfredo@gmail.com"), 20)
        student2 = Student("Osvaldo de Sousa", Email("osvaldo@gmail.com"), 20)
        student3 = Student("Bislânia de Sousa", Email("bis@gmail.com"), 20)

        classroomPolicy = ClassroomPolicy
        enrollmentRepository = EnrollmentRepository()
        classroomRepository = ClassroomRepository()
        enrollmentService = EnrollmentService(classroomRepository, enrollmentRepository, classroomPolicy)
        
        enrollmentService.enroll(student1)
        enrollmentService.enroll(student2)
        enrollmentService.enroll(student3)

        allClassrooms = classroomRepository.get_classrooms()

        self.assertEqual(len(allClassrooms), 0)

if __name__ == "__main__":
    unittest.main()