from enrollment.domain.model.student import Student
from typing import List
from enrollment.domain.ports.driven.enrollment_repository import IEnrollmentRepository

class EnrollmentRepository(IEnrollmentRepository): 
    def __init__(self):
        self.enrolled_students: List["Student"] = []

    def save(self, student: "Student"):         
        emails = [s.email for s in self.enrolled_students]
        
        if not student.email in emails:
            self.enrolled_students.append(student)

    def getAll(self):
        return list(self.enrolled_students)

    def clear(self):
        self.enrolled_students = []
