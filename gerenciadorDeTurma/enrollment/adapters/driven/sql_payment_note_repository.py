import sqlite3
from enrollment.domain.ports.driven.payment_note_repository import IPaymentNoteRepository
from enrollment.domain.model.payment_note import PaymentNote
from enrollment.domain.model.student import Student

class SQLitePaymentNoteReository(IPaymentNoteRepository):
    def __init__(self, db_path="enrollment.db") -> None:
        super().__init__()
        self.conn = sqlite3.connect(db_path)
        self._create_table()
        
    def _create_table(self):
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS payment_notes (
                id TEXT PRIMARY KEY,
                price INTEGER,
                dueDate TEXT,
                id_student TEXT,
                FOREIGN KEY (id_student) REFERENCES enrolled_students(id)
            )""")
    
    def save(self, paymentNote: "PaymentNote"):
        with self.conn:
            self.conn.execute("""
            INSERT OR IGNORE INTO payment_notes (
                id,
                price,
                dueDate,
                id_student
            ) VALUES (?,?,?,?)
            """, (
                paymentNote.id,
                paymentNote.price,
                paymentNote.dueDate,
                paymentNote.idStudent    
            ))

   
    def getAll(self):
        cursor = self.conn.cursor()
        cursor.execute("""
                    SELECT 
                       payment_notes.id AS payment_note_id, 
                       payment_notes.price AS payment_note_price, 
                       payment_notes.dueDate AS payment_note_due_date, 
                       enrolled_students.name AS student_name 
                    FROM payment_notes
                    INNER JOIN enrolled_students 
                    ON enrolled_students.id = payment_notes.id_student """)
        rows = cursor.fetchall()
        payment_notes = []
        
        for row in rows:
            payment_note = PaymentNote(
                price = row[1],
                dueDate = row[2],
                idStudent = row[3] 
            )
            id = row[0]
            
            payment_notes.append(payment_note)
        
        cursor.close()
        
        return payment_notes
    