from enrollment.student import Student

class WaitingListRepository(): 
    def __init__(self):
        self.waiting_students = []

    def add_waiting_student(self, student: "Student"):
        self.waiting_students.append(student)

    def get_waiting_student(self):
        return self.waiting_students

    def clear_waiting_list(self):
        self.waiting_students = []
