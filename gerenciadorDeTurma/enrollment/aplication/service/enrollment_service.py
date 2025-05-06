from enrollment.domain.ports.driving.enrollment import IEnrollment
from enrollment.domain.model.student import Student
from enrollment.domain.model.classroom import Classroom
from enrollment.domain.ports.driving.enrollment import IEnrollment
from enrollment.domain.ports.driven.classroom_repository import IClassroomRepository
from enrollment.domain.ports.driven.enrollment_repository import IEnrollmentRepository
from enrollment.domain.ports.driven.event_bus_publisher import IEventBusPublisher
from enrollment.domain.ports.driven.payment_note_repository import IPaymentNoteRepository

from enrollment.domain.events.events import events
from enrollment.domain.policy.classroom_policy import ClassroomPolicy
from typing import List

 
class EnrollmentService(IEnrollment):
    def __init__(self, classroomRepository: IClassroomRepository, classroomPolicy:ClassroomPolicy, enrollmentRepository: IEnrollmentRepository, event_bus: IEventBusPublisher):
        self.classroomRepository = classroomRepository
        self.enrollmentRepository = enrollmentRepository
        self.policy = classroomPolicy
        self.event_bus = event_bus

    def enroll(self, name, email, age):
        student = Student(name, email, int(age))
        self.enrollmentRepository.save(student)
        self.event_bus.publish(events.studentEnrolled, {name, email, age})
        
        print("\n=================================")
        print("==> Sucesso: Usuário inscrito <==")
        print("=================================\n")
        
        if self.policy.shouldCreateClassroom(len(self.enrollmentRepository.getNotRegisteredStudents())):
            studentsEnrolled = self.enrollmentRepository.getNotRegisteredStudents()

            newClassroom = Classroom(studentsEnrolled)
            self.save_classroom_in_repository(newClassroom)

    def save_classroom_in_repository(self, classroom: "Classroom"):
        self.classroomRepository.save(classroom.id)
        self.enrollmentRepository.updateClassroomId(classroom.id)

        print("\n================================")
        print("==>  Sucesso: Turma criada   <==")
        print("================================\n")
            
        self.event_bus.publish(events.classRoomCreated, classroom)
        
    def getAllStudents(self) -> List[Student]:
        return self.enrollmentRepository.getAll()
    
    def getAllClassroom(self) -> List[Classroom]:
        return self.classroomRepository.getAll()
