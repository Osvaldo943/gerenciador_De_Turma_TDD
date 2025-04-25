from enrollment.aplication.service.enrollment_service import EnrollmentService
from enrollment.domain.model.student import Student
from enrollment.utils.clean_screen import clean_screen
class CLI: 
    def __init__(self, enrollmentService: EnrollmentService):
        self.enrollmentService = enrollmentService

    def run(self): 
        while True:
            print("\n=========Opções=========")
            print("\n1--> Fazer inscrição") 
            print("2--> Listar Alunos")
            print("3--> Listar Turmas")
            print("4--> Sair")
            
            option = input("\n==> ")
            clean_screen()
            try:
                if(option == '1'):
                    print("1-Inscrição de aluno \n")
                    name = input("\nDigite o teu nome: ")
                    email = input("Digite o teu email: ")
                    age = int(input("Digite a tua idade: "))
                    
                    self.enrollmentService.enroll(name, email, age)    
                
                if(option == '2'):
                    print("2-Lista de inscritos")
                    
                    print(f"{'ID':>0} {'Nome':>32} {'Email':>30} {'Idade':>30} {'Registrado':>30}")
                    print('-' * 100)
                    allStudents = self.enrollmentService.getAllStudents()
                    
                    for student in allStudents:
                        print(f"{student.id:<30} {student.name:<30} {student.email.value():<30} {student.age :<30} {str(student.classroom_id):<30}")
                        
                if(option == '3'):
                    print("\n3-Lista de turmas criadas:")
                
                    allClassroom = self.enrollmentService.getAllClassroom()
                    
                    for classroom in allClassroom:
                        print("Turma: ", classroom.getId()) 
                        
                        print(f"{'ID':>0} {'Nome':>32} {'Email':>30} {'Idade':>30} ")
                        print('-' * 100)
                        for student in classroom.getStudents():
                            print(student.name, student.age, student.email.value())
                                        
   
            except ValueError as e:
                print(f"Erro -> ", {e})    
        
            except Exception as e:
                print(f"Erro na Exception", {e})  