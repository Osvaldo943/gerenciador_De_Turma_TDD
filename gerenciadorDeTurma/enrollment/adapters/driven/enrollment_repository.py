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
            
    def getNotRegisteredStudents(self):
        self.not_registered_students = []
        
        for student in self.enrolled_students:
            if student.classroom_id == None:
                self.not_registered_students.append(student)
            
        return list(self.not_registered_students)
    
    def updateClassroomId(self, classroom_id):
        pass 
    
    def getAll(self)->List[Student]:
        return list(self.enrolled_students)

    def clear(self):
        self.enrolled_students = []
