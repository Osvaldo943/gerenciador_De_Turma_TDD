import {assertEquals} from "jsr:@std/assert/equals"
import { eventBus } from "./eventBus.ts"
import { EnrollmentService, ClassroomRepository, PaymentNoteService, Student, WaitingListRepository, NotifyStudentService } from "./service_enrollment.ts"
import { Classroom } from "./Classroom.ts";
import { PaymentNoteRepository } from "./service_enrollment.ts";


Deno.test("Deve disparar o evento turma_criada quando a turma for criada", ()=>{
    const classRoom: Classroom = {
        id: "II10A",
        students:[
        new Student("00234LA21A0", "Joel dos Santos", 24), 
        new Student ("00234LA21A0","Osvaldo de Sousa",24)
    ]}

    let isClassroomCreated = false
    
    eventBus.subscribe("classroomCreated", ()=>{
        isClassroomCreated = true
    })

    const waitingListRepository  = new WaitingListRepository()
    const classRoomRepository = new ClassroomRepository()
    const notifyStudentService = new NotifyStudentService()
    const service = new EnrollmentService(classRoomRepository, waitingListRepository, notifyStudentService)
    
    service.createClassRoom(classRoom)
    
    assertEquals(isClassroomCreated, true)
})

Deno.test("Deve registar a turma no repositório", ()=>{
    const classRoom = {
        id: "II10B",
        students:[
        new Student("00234LA21A0", "Joel dos Santos", 24), 
        new Student ("00234LA21A0","Osvaldo de Sousa",24)
    ]}

    const waitingListRepository  = new WaitingListRepository()
    const classRoomRepository = new ClassroomRepository()
    const notifyStudentService = new NotifyStudentService()
    const service = new EnrollmentService(classRoomRepository, waitingListRepository, notifyStudentService)

    service.createClassRoom(classRoom)
    const turmas = classRoomRepository.getClassroom()
    
    assertEquals(turmas.length, 1)
    assertEquals(turmas[0].id, "II10B")
    assertEquals(turmas[0].students.length, 2)
})


Deno.test("Deve gerar notas de pagamento quando o evento Turma_Criada for gerado", ()=>{
    const classRoom = {
        id: "II10A",
        students:[
        new Student("00234LA21A0", "Joel dos Santos", 24), 
        new Student ("00234LA21A0","Osvaldo de Sousa",24)
    ]}

    const paymentNoteRepository = new PaymentNoteRepository()
    const paymentService = new PaymentNoteService(paymentNoteRepository)

    eventBus.subscribe("classroomCreated", (newClassRoom)=>{
        paymentService.generatePaymentNote(newClassRoom)
    })

    const waitingListRepository  = new WaitingListRepository()
    const classRoomRepository = new ClassroomRepository()
    const notifyStudentService = new NotifyStudentService()
    const service = new EnrollmentService(classRoomRepository, waitingListRepository, notifyStudentService)

    service.createClassRoom(classRoom)

    assertEquals(paymentNoteRepository.getPaymentNotes().length, 1)
})

Deno.test("Deve disparar o evento aluno_Inscrito quando o aluno for adicionado na lista de espera", ()=>{
    const newStudent = new Student("00234LA21A0","Joel dos Santos", 24)
    let isStudentAdded = false

    eventBus.subscribe("StudentAdded", ()=>{
        isStudentAdded = true
    })
    
    const maxNumberOfStudents = 4

    const waitingListRepository  = new WaitingListRepository()
    const classRoomRepository = new ClassroomRepository()
    const notifyStudentService = new NotifyStudentService()
    const service = new EnrollmentService(classRoomRepository, waitingListRepository, notifyStudentService)

    service.addStudent(newStudent, maxNumberOfStudents)
    
    assertEquals(isStudentAdded, true)
})

Deno.test("Deve criar turma quando a lista de espera tiver alunos suficiente", ()=>{
    const newStudent1 = new Student("00234LA21A0","Joel dos Santos", 24)
    const newStudent2 = new Student("10234LA21A0","Joelson dos Santos", 24)
    const newStudent3 = new Student("20234LA21A0","Jão dos Santos", 24)
    const newStudent4 = new Student("30234LA21A0","Camaro dos Santos", 24)

    const waitingListRepository = new WaitingListRepository()
    const classRoomRepository = new ClassroomRepository()
    const notifyStudentService = new NotifyStudentService()
    const service = new EnrollmentService(classRoomRepository, waitingListRepository, notifyStudentService)

    const maxNumberOfStudent = 4
    service.addStudent(newStudent1, maxNumberOfStudent)
    service.addStudent(newStudent2, maxNumberOfStudent)
    service.addStudent(newStudent3, maxNumberOfStudent)
    service.addStudent(newStudent4, maxNumberOfStudent)

    const turmas = classRoomRepository.getClassroom()

    assertEquals(turmas.length, 1)
})

Deno.test("Deve vaziar a lista de alunos em espera quando a turma for criada", ()=>{
    const newStudent1 = new Student("00234LA21A0","Joel dos Santos", 24)
    const newStudent2 = new Student("10234LA21A0","Joelson dos Santos", 24)
    const newStudent3 = new Student("20234LA21A0","Jão dos Santos", 24)
    const newStudent4 = new Student("30234LA21A0","Camaro dos Santos", 24)

    const waitingListRepository = new WaitingListRepository()
    const classRoomRepository = new ClassroomRepository()
    const notifyStudentService = new NotifyStudentService()
    const service = new EnrollmentService(classRoomRepository, waitingListRepository, notifyStudentService)

    const maxNumberOfStudent = 4
    service.addStudent(newStudent1, maxNumberOfStudent)
    service.addStudent(newStudent2, maxNumberOfStudent)
    service.addStudent(newStudent3, maxNumberOfStudent)
    service.addStudent(newStudent4, maxNumberOfStudent)

    const classRooms = classRoomRepository.getClassroom()
    const waitingList = waitingListRepository.getStudents()

    assertEquals(classRooms.length, 1)
    assertEquals(waitingList.length, 0)
}) 



Deno.test("Deve notificar alunos quando a turma for criada", ()=>{
    const newStudent1 = new Student("00234LA21A0","Joel dos Santos", 24)
    const newStudent2 = new Student("10234LA21A0","Joelson dos Santos", 24)
    const newStudent3 = new Student("20234LA21A0","Jão dos Santos", 24)
    const newStudent4 = new Student("30234LA21A0","Camaro dos Santos", 24)

    const waitingListRepository = new WaitingListRepository()
    const classRoomRepository = new ClassroomRepository()
    const notifyStudentService = new NotifyStudentService()
    const service = new EnrollmentService(classRoomRepository, waitingListRepository, notifyStudentService)

    const maxNumberOfStudent = 4
    service.addStudent(newStudent1, maxNumberOfStudent)
    service.addStudent(newStudent2, maxNumberOfStudent)
    service.addStudent(newStudent3, maxNumberOfStudent)
    
    eventBus.subscribe("classroomCreated", (classroom:Classroom)=>{
        classroom.students.map((student)=>{
            assertEquals(student.isNotified, true)
        })
    })
    
    service.addStudent(newStudent4, maxNumberOfStudent)

    const classRooms = classRoomRepository.getClassroom()
    const waitingList = waitingListRepository.getStudents()

    assertEquals(classRooms.length, 1)
    assertEquals(waitingList.length, 0)
}) 


