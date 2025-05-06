import sqlite3
from enrollment.domain.ports.driven.classroom_repository import IClassroomRepository
from enrollment.domain.model.classroom import Classroom
from enrollment.domain.model.student import Student
from enrollment.domain.model.email import Email

class SQLiteclassroomRepository(IClassroomRepository):
    def __init__(self, db_path="enrollment.db") -> None:
        super().__init__()
        self.conn = sqlite3.connect(db_path)
        self._create_table()
        
    def _create_table(self):
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS classrooms (
                id TEXT PRIMARY KEY
            )
            """)
            
    def save(self, classroom_id):
        with self.conn:
            self.conn.execute("""
            INSERT OR IGNORE INTO classrooms (id) VALUES (?)
            """,(classroom_id,))
            
    def getAll(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT classrooms.id AS classroom_id, 
            enrolled_students.id AS student_id, 
            enrolled_students.name AS student_name, 
            enrolled_students.email AS student_email, 
            enrolled_students.age AS student_age, 
            enrolled_students.is_notified AS student_is_notified 
        FROM classrooms 
        INNER JOIN enrolled_students 
        ON enrolled_students.classroom_id = classrooms.id
        """)
        rows = cursor.fetchall()
        classrooms_dict = {}

        for row in rows:
            classroom_id, student_id, student_name, student_email, student_age, student_is_notified = row
            
            if classroom_id not in classrooms_dict: 
                classrooms_dict[classroom_id] = {
                    "id": classroom_id,
                    "students": []
                }
            
            student = Student(name=student_name, email=Email(student_email), age=student_age)
            student.id = student_id
            student.isNotified = bool(student_is_notified)
            student.classroom_id = classroom_id
            
            classrooms_dict[classroom_id]["students"].append(student)

        cursor.close()
        
        classrooms = []

        for classroom_id, students in classrooms_dict.items():
            classroom = Classroom(students["students"])  
            classroom.id = classroom_id
            classrooms.append(classroom)
        
        return classrooms
