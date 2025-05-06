from enrollment.domain.model.classroom import Classroom
from enrollment.domain.events.events import events
from enrollment.domain.ports.driven.event_bus_publisher import IEventBusPublisher

class NotificationService(): 
    def __init__(self, eventBus: IEventBusPublisher) -> None:
        self.eventBus = eventBus 
        
    def notify(self, classroom: "Classroom"): 
        for student in classroom.students:
            student.mark_as_notified()
            print(student.name, " notificado")

        self.eventBus.publish(events.studentNotified, classroom)
