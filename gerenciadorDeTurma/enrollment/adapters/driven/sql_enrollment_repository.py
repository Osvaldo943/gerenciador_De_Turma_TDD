import sqlite3
from enrollment.domain.ports.driven.enrollment_repository import IEnrollmentRepository
from enrollment.domain.model.student import Student
from enrollment.domain.model.email import Email
from enrollment.domain.model.classroom import Classroom

class SQLiteEnrollmentRepository(IEnrollmentRepository):
    def __init__(self, db_path="enrollment.db") -> None:
        super().__init__()
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS enrolled_students (
                id TEXT PRIMARY KEY,
                name TEXT, 
                email TEXT UNIQUE, 
                age INTEGER, 
                is_notified BOOLEAN,
                classroom_id TEXT,
                FOREIGN KEY (classroom_id) REFERENCES classrooms(id)
            )
            """)

    def save(self, student: "Student"):
        with self.conn:
            self.conn.execute("""
            INSERT OR IGNORE INTO enrolled_students (
                id, 
                name, 
                email, 
                age, 
                is_notified,
                classroom_id
            ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                student.id, 
                student.name, 
                student.email, 
                student.age, 
                student.isNotified, 
                None 
            ))

    def getAll(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, email, age, is_notified, classroom_id from enrolled_students")
        rows = cursor.fetchall()
        students =  []
        
        for row in rows: 
            student = Student(name= row[1], email=Email(row[2]), age=row[3])
            student.id = row[0]
            student.isNotified = bool(row[4])
            student.classroom_id = row[5] 
            students.append(student)

        return students

    def getNotRegisteredStudents(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, email, age, is_notified, classroom_id FROM enrolled_students WHERE classroom_id IS NULL")
        rows = cursor.fetchall()

        notRegisteredStudents = []

        for row in rows: 
            student = Student(name= row[1], email=Email(row[2]), age=row[3])
            student.id = row[0]
            student.isNotified = bool(row[4])
            student.classroom_id = row[5]  
            notRegisteredStudents.append(student)

        return notRegisteredStudents

    def updateClassroomId(self, classroom_id):
        query = """
                UPDATE enrolled_students 
                SET classroom_id = ?
                WHERE classroom_id IS NULL
            """

        with self.conn:
            self.conn.execute(query, (classroom_id,))

    def clear(self):
        with self.conn:
            self.conn.execute("DELETE FROM enrolled_students")
