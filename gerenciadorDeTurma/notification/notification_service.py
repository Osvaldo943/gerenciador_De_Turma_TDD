from enrollment.classroom import Classroom
from event_bus import event_bus

class NotifyStudentService(): 
    def notify(self, classroom: "Classroom"): 
        for student in classroom.students:
            student.isNotified = True
            print(student.name+" foi notificado")

        event_bus.publish("studentsNotified", classroom)
