from enrollment.student import Student
from typing import List
from event_bus import event_bus
from event_bus import events

class WaitingListRepository(): 
    def __init__(self):
        self.waiting_students: List["Student"] = []

    def add_waiting_student(self, student: "Student"):         
        emails = [s.email for s in self.waiting_students]
        
        if not student.email in emails:
            self.waiting_students.append(student)
            event_bus.publish(events.studentEnrolled, student)

    def get_waiting_students(self):
        return list(self.waiting_students)

    def clear_waiting_list(self):
        self.waiting_students = []
