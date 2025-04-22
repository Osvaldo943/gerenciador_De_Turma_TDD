from enrollment.domain.model.classroom import Classroom
from enrollment.shared.event_bus import event_bus
from enrollment.shared.event_bus import events

class NotifyStudentService(): 
    def notify(self, classroom: "Classroom"): 
        for student in classroom.students:
            student.mark_as_notified()

        event_bus.publish(events.studentNotified, classroom)
