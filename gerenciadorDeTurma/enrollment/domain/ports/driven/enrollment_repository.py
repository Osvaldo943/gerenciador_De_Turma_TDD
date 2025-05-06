from abc import ABC, abstractmethod
from enrollment.domain.model.student import Student
from typing import List

class IEnrollmentRepository(ABC):
    
    @abstractmethod
    def save(self, student: Student):
        pass 
    
    @abstractmethod
    def getAll(self)-> List[Student]:
        pass
    
    @abstractmethod
    def getNotRegisteredStudents(self) -> List[Student]:
        pass
    
    @abstractmethod
    def updateClassroomId(self, classroom_id) -> None:
        pass
    
    @abstractmethod
    def clear(self)-> List[Student]:
        pass
    