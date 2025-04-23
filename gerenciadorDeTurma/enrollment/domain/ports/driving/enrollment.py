from abc import ABC, abstractmethod
from enrollment.domain.model.student import Student

class IEnrollment(ABC):
    
    @abstractmethod
    def enroll(self, student: Student):
        pass
    
    @abstractmethod
    def save_classroom_in_repository(self, student: Student):
        pass