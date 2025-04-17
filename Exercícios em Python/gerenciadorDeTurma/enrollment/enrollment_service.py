from event_bus import event_bus
from enrollment.classroom_repository import ClassroomRepository
from enrollment.student import Student
from enrollment.classroom import Classroom
from enrollment.waiting_list_repository import WaitingListRepository
from event_bus import events

MAXIMUM_NUMBER_OF_STUDENTS = 4

class EnrollmentService():

    def __init__(self, repository: "ClassroomRepository", waitingListRepository: "WaitingListRepository"):
        self.repository = repository
        self.waitingListRepository: WaitingListRepository = waitingListRepository

    def enroll(self, student: "Student"):
        self.waitingListRepository.add_waiting_student(student)
        quantityOfStudents = len(self.waitingListRepository.get_waiting_students())
       
        if(quantityOfStudents == MAXIMUM_NUMBER_OF_STUDENTS):
            studentsWaiting = self.waitingListRepository.get_waiting_students()
            newClassroom = Classroom(studentsWaiting)
            self.create_classroom(newClassroom)
            self.waitingListRepository.clear_waiting_list()
        
    def create_classroom(self, classroom: "Classroom"):
        self.repository.save_classroom(classroom)
        event_bus.publish(events.classRoomCreated, classroom)

