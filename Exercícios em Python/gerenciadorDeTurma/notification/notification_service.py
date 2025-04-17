from enrollment.classroom import Classroom
from event_bus import event_bus
from event_bus import events

class NotifyStudentService(): 
    def notify(self, classroom: "Classroom"): 
        for student in classroom.students:
            student.notifiedStudent()

        event_bus.publish(events.studentNotified, classroom)
