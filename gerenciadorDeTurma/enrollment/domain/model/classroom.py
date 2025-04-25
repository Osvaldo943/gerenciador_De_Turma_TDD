from enrollment.domain.model.student import Student
import uuid
from typing import List

MAXIMUM_NUMBER_OF_STUDENTS = 4

class Classroom():
    def __init__(self, students: List["Student"]):

        if not self.has_enough_students(len(students)):
            raise ValueError("Quantidade de aluno incorreta")
        
        self.id = int(str(uuid.uuid4().int)[:8])
        self.students: list[Student] = students

    def has_enough_students(self, numberOfStudent: int):
        return numberOfStudent == MAXIMUM_NUMBER_OF_STUDENTS
    
    def getId(self):
        return str(self.id)
    
    def getStudents(self):
        return list(self.students)
            
