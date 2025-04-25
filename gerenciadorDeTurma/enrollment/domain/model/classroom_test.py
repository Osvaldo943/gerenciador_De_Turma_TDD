import unittest
from enrollment.domain.model.classroom import Classroom
from enrollment.domain.model.student import Student 
from enrollment.domain.model.student import Email 
from enrollment.domain.policy.classroom_policy import ClassroomPolicy
from enrollment.domain.model.classroom import MAXIMUM_NUMBER_OF_STUDENTS

class testes(unittest.TestCase):
    def setUp(self): 
        self.students: list[Student] = [
            Student("Joelson dos Santos", Email("joelson@gmail.com"), 24),
            Student("Osvaldo dos Santos", Email("osvaldo@gmail.com"), 24),
            Student("Lemos dos Santos", Email("lemos@gmail.com"), 24),
            Student("Rui dos Santos", Email("rui@gmail.com"), 24),
        ]

        self.less_students_than_enough = self.students[:MAXIMUM_NUMBER_OF_STUDENTS - 1]
        self.more_students_than_enough = self.students + [Student("Domingos dos Santos", Email("domingos@gmail.com"), 40)]

    def test_criar_turma(self):
        """"Deve criar turma"""

        newClassroom = Classroom(self.students)

        self.assertIsNotNone(newClassroom.id)
        self.assertEqual(newClassroom.students, self.students)
        
    def test_valueError_deve_emitir_erro_aluno_insuficiente(self):
        """"Deve criar turma"""

        with self.assertRaises(ValueError) as cm:
            classroom = Classroom(self.less_students_than_enough)

        self.assertEqual(str(cm.exception), "Quantidade de aluno incorreta")
    
    def test_valueError_deve_emitir_erro_aluno_mais_do_que_suficiente(self):
        """"Deve emitir erro alunos mais do que suficiente quando adicionamos mais de 4 alunos numa turma"""
        with self.assertRaises(ValueError) as cm:
            classroom = Classroom(self.more_students_than_enough)

        self.assertEqual(str(cm.exception), "Quantidade de aluno incorreta")
    
    def test_deve_retornar_false_para_quantidade_de_alunos_inferior(self):
        """"Deve retornar False quando a lista de alunos for insuficiente"""
        classroom = Classroom(self.students)
        self.assertFalse(classroom.has_enough_students(self.students[:MAXIMUM_NUMBER_OF_STUDENTS - 1]))
        
    def test_deve_retornar_false_para_quantidade_de_alunos_inferior(self):
        """"Deve retornar True quando a lista de alunos for suficiente (4)"""
        classroom = Classroom(self.students)
        self.assertTrue(classroom.has_enough_students(len(self.students)))
        
    def test_deve_retornar_false_para_quantidade_de_alunos_inferior(self):
        """"Deve retornar False quando a lista de alunos for mais do que suficiente (> 4)"""
        classroom = Classroom(self.students)
        self.assertFalse(classroom.has_enough_students(len(self.more_students_than_enough)))
    
    def test_getStudents_deve_retornar_lista_de_estudante(self):
        """getStudents deve retornar lista de estudante"""
        
        classroom = Classroom(self.students)
        self.assertEqual(classroom.getStudents(), self.students)
    
    def test_getId_deve_retornar_Id_da_turma(self):
        """getId deve retornar id da turma"""
        
        classroom = Classroom(self.students)
        self.assertIsNotNone(classroom.getId())
        
