from enrollment.domain.model.student import Student
import uuid
from typing import List
from enrollment.domain.policy.classroom_policy import ClassroomPolicy

class Classroom():
    def __init__(self, students: List["Student"]):
        self.classroomPolicy = ClassroomPolicy()

        if not self.has_enough_students(len(students)):
            raise ValueError("Quantidade de aluno incorreta")
        
        self.id = int(str(uuid.uuid4().int)[:8])
        self.students: list[Student] = students

    def has_enough_students(self, numberOfStudent: int):
        return self.classroomPolicy.shouldCreateClassroom(numberOfStudent)
    
    def getId(self):
        return str(self.id)
    
    def getStudents(self)-> List["Student"]:
        return list(self.students)
            
