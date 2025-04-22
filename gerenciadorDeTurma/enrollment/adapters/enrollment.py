from enrollment.domain.ports.enrollment import IEnrollment
from enrollment.domain.repository.enrollment_repository import EnrollmentRepository
from enrollment.domain.model.student import Student

class CLI(IEnrollment): 
    def __init__(self, enrollmentRepository: EnrollmentRepository):
        self.enrollmentRepository = enrollmentRepository
        
    def  enroll(self):
        name = print("Digite o teu nome")
        email = print("Digite o teu email")
        age = print("Digite a tua idade")
        