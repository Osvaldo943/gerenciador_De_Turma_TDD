from enrollment.domain.model.student import Student
from typing import List
from enrollment.shared.event_bus import event_bus
from enrollment.shared.event_bus import events

class EnrollmentRepository(): 
    def __init__(self):
        self.enrolled_students: List["Student"] = []

    def add_waiting_student(self, student: "Student"):         
        emails = [s.email for s in self.enrolled_students]
        
        if not student.email in emails:
            self.enrolled_students.append(student)
            event_bus.publish(events.studentEnrolled, student)

    def get_enrolled_students(self):
        return list(self.enrolled_students)

    def clear_enrolled_students(self):
        self.enrolled_students = []
