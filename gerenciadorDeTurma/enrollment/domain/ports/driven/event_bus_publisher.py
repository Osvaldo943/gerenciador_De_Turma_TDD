from abc import ABC, abstractmethod

class IEventBusPublisher(ABC): 
    
    @abstractmethod
    def publish(self)->None: 
        pass
