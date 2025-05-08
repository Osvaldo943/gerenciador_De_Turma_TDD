from enrollment.domain.model.student import Student

class EmailSender():
    def notify(self, receptor: Student):
        print("Enviando email para ", receptor.name,"...") 