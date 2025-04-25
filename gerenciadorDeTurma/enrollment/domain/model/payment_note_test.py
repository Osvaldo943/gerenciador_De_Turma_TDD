from enrollment.domain.model.payment_note import PaymentNote
from enrollment.domain.model.student import Student
import unittest

class testes(unittest.TestCase):
    def setUp(self): 
        pass

    def test_criar_nota_de_pagamento(self):
        newStudent = Student("Joel Rosa", "joel@gmail.com", 22)
        payment_note = PaymentNote(newStudent.id, 5000, "12-05-2025")
        
        self.assertIsNotNone(payment_note.id)
        self.assertEqual(payment_note.price, 5000)
        self.assertEqual(payment_note.dueDate, "12-05-2025")
        
        