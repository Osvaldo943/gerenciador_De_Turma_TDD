from enrollment.student import Student
import uuid

class Classroom():
    def __init__(self, students):
        self.id = int(str(uuid.uuid4().int)[:8])
        self.students: list[Student] = students
