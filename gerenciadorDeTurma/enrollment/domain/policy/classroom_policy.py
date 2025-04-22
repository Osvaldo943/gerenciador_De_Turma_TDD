
MAXIMUM_NUMBER_OF_STUDENTS = 4

class ClassroomPolicy():
    def shouldCreateClassroom(self, numberOfEnrolledStudents: int) -> bool:
        return numberOfEnrolledStudents == MAXIMUM_NUMBER_OF_STUDENTS
    