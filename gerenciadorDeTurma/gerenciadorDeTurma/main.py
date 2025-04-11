from event_bus import event_bus
import uuid

class EnrollmentService():
    def __init__(self, repository: "Repository", waitingListRepository: "WaitingListRepository"):
        self.repository = repository
        self.waitingListRepository = waitingListRepository

    def enroll(self, student: "Student"):
        self.waitingListRepository.save_student(student)
        event_bus.publish("studentEnrolled", student)

        quantityOfStudents = len(self.waitingListRepository.get_student())

        if(quantityOfStudents == 4):
            studentsWaiting = self.waitingListRepository.get_student()
            newClassroom = Classroom(studentsWaiting)
            self.create_classroom(newClassroom)
            self.waitingListRepository.clear_waiting_list()
        
    def create_classroom(self, classroom: "Classroom"):
        self.repository.save_classroom(classroom)
        event_bus.publish("classroomCreated", classroom)


class Classroom():
    def __init__(self, students):
        self.id = int(str(uuid.uuid4().int)[:8])
        self.students: list[Student] = students
        
class Repository():
    def __init__(self):
        self.classrooms: list[Classroom] = [] 

    def save_classroom(self, classroom: Classroom):
        self.classrooms.append(classroom)
    
    def get_classroom(self):
        return self.classrooms


class Student(): 
    def __init__(self, name, email, age):
        self.id = int(str(uuid.uuid4().int)[:8])
        self.name = name
        self.email = email
        self.age = age
        self.isNotified = False
        

class NotifyStudentService(): 

    def notify(self, classroom: "Classroom"): 
        for student in classroom.students:
            student.isNotified = True
            print(student.name+" foi notificado")

        event_bus.publish("studentsNotified", classroom)


class WaitingListRepository(): 
    def __init__(self):
        self.waitingList = []

    def save_student(self, student: "Student"):
        self.waitingList.append(student)

    def get_student(self):
        return self.waitingList

    def clear_waiting_list(self):
        self.waitingList = []