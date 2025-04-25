import sqlite3
from enrollment.domain.ports.driven.classroom_repository import IClassroomRepository
from enrollment.domain.model.classroom import Classroom

class SQLiteclassroomRepository(IClassroomRepository):
    def __init__(self, db_path="enrollment.db") -> None:
        super().__init__()
        self.conn = sqlite3.connect(db_path)
        self._create_table()
        
    def _create_table(self):
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS classrooms (
                id TEXT PRIMARY KEY,
            )
            """)
            
    def save(self, classroom_id):
        with self.conn:
            self.conn.execute("""
            INSERT OR IGNORE INTO classrooms (id) VALUES (?)
            """,(classroom_id))