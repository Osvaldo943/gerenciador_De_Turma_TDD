from enrollment.domain.model.classroom import Classroom
from typing import List

class ClassroomRepository():
    def __init__(self):
        self.classrooms: list[Classroom] = [] 

    def save(self, classroom: Classroom):
        self.classrooms.append(classroom)
    
    def getAll(self) -> List[Classroom]:
        return list(self.classrooms)
