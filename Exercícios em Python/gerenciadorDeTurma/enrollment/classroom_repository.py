from enrollment.classroom import Classroom

class ClassroomRepository():
    def __init__(self):
        self.classrooms: list[Classroom] = [] 

    def save_classroom(self, classroom: Classroom):
        self.classrooms.append(classroom)
    
    def get_classrooms(self):
        return self.classrooms
