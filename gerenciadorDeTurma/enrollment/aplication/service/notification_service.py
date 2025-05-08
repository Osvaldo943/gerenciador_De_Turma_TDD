from enrollment.domain.model.classroom import Classroom
from enrollment.domain.events.events import events
from enrollment.domain.ports.driven.event_bus_publisher import IEventBusPublisher
from enrollment.domain.ports.driven.notification import INotification
   
class NotificationService():  
    def __init__(self, notification: INotification, eventBus: IEventBusPublisher) -> None:
        self.eventBus = eventBus 
        self.notification = notification
        
    def notify(self, classroom: "Classroom"): 
        for student in classroom.students:
            student.mark_as_notified()
            self.notification.notify(student)
            
        self.eventBus.publish(events.studentNotified, classroom)
