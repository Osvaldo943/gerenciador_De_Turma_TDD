from enrollment.shared.event_bus import event_bus
from enrollment.domain.repository.classroom_repository import ClassroomRepository
from enrollment.domain.model.student import Student
from enrollment.domain.model.classroom import Classroom
from enrollment.domain.repository.enrollment_repository import EnrollmentRepository
from enrollment.shared.event_bus import events
from enrollment.domain.policy.classroom_policy import ClassroomPolicy
from typing import List

class EnrollmentService():
    def __init__(self, repository: "ClassroomRepository", enrollmentRepository: "EnrollmentRepository", policy: "ClassroomPolicy"):
        self.repository = repository
        self.enrollmentRepository: EnrollmentRepository = enrollmentRepository
        self.policy = policy

    def enroll(self, student: "Student"):
        self.enrollmentRepository.add_waiting_student(student)
        
        if(self.policy.shouldCreateClassroom(self, len(self.enrollmentRepository.get_enrolled_students()))):
            studentsWaiting = self.enrollmentRepository.get_enrolled_students()

            newClassroom = Classroom(studentsWaiting)
            self.save_classroom_in_repository(newClassroom)
            self.enrollmentRepository.clear_enrolled_students()
        
    def save_classroom_in_repository(self, classroom: "Classroom"):
        self.repository.save_classroom(classroom)
        event_bus.publish(events.classRoomCreated, classroom)
