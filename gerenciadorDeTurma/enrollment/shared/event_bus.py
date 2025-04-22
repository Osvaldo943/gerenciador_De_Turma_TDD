class Events ():
    def __init__(self):    
        self.classRoomCreated= "ClassRoomCreated"
        self.studentEnrolled= "studentEnrolled"    
        self.studentRegistered= "studentRegistered"
        self.studentNotified= "studentNotified" 


class EventBus:
    def __init__(self):
        self.handlers = {}

    def subscribe(self, event, handler):
        if event not in self.handlers:
            self.handlers[event] = []
        self.handlers[event].append(handler)

    def publish(self, event, payload):
        if event in self.handlers:
            for handler in self.handlers[event]:
                handler(payload)

event_bus = EventBus()
events = Events()
