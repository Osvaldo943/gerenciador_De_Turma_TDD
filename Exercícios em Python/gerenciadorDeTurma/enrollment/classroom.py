from enrollment.student import Student
import uuid
from typing import List

MAXIMUM_NUMBER_OF_STUDENTS = 4

class Classroom():
    def __init__(self, students: List["Student"]):

        if self.has_not_enough_students(len(students)):
            raise ValueError("Alunos insuficiente")

        self.id = int(str(uuid.uuid4().int)[:8])
        self.students: list[Student] = students

    def has_not_enough_students(self, numberOfStudent: int):
        return numberOfStudent != MAXIMUM_NUMBER_OF_STUDENTS
            
