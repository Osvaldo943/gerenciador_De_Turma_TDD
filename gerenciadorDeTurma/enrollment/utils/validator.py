import re 

def validator(name, email, age):
    if name == '':
        return print("O campo nome é obrigatório")
            
    if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        return print("Email inválido")
        
    if not age >= 0:
        return print("Idade não válida")