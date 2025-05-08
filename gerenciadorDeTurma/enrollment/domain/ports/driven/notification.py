from abc import ABC, abstractmethod
from enrollment.domain.model.student import Student
 
class INotification(ABC):
    
    @abstractmethod
    def notify(self, Student: "Student"):
        pass