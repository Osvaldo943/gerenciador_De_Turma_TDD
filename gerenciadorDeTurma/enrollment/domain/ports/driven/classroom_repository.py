from abc import ABC, abstractmethod
from enrollment.domain.model.classroom import Classroom

class IClassroomRepository(ABC):
    
    @abstractmethod
    def save(self, classroom: Classroom):
        pass
    
    @abstractmethod
    def getAll(self):
        pass