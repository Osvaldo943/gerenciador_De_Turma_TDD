import { Classroom } from "./Classroom.ts";
import { PaymentNote } from "./PaymentNote.ts";
import { eventBus} from "./eventBus.ts";

export class EnrollmentService {
    classroomRepository: ClassroomRepository
    waitingListRepository: WaitingListRepository
    notifyStudentService: NotifyStudentService

    constructor(classroomRepository: ClassroomRepository, waitingListRepository: WaitingListRepository, notifyStudentService: NotifyStudentService){
        this.waitingListRepository = waitingListRepository
        this.classroomRepository = classroomRepository
        this.notifyStudentService = notifyStudentService
    }

    createClassRoom(classRoom: Classroom){
        
        this.classroomRepository.saveClassroom(classRoom)

        this.notifyStudentService.notify(classRoom)
        
        eventBus.publish("classroomCreated", classRoom)
    }

    addStudent(student: Student, maxNumberOfStudents: number){
        this.waitingListRepository.saveStudent(student)
        
        const quantityOfStudents = this.waitingListRepository.getStudents().length

        if(quantityOfStudents == maxNumberOfStudents){
            const classroom: Classroom = {
                id: Math.floor(Math.random()*1000).toString(), 
                students: this.waitingListRepository.getStudents()
            }

            this.createClassRoom(classroom)

            this.waitingListRepository.clear()
            
            eventBus.publish("StudentAdded", student)

            return classroom
        }

        eventBus.publish("StudentAdded", student)
    }
}

export class PaymentNoteService {
    paymentNoteRepository: PaymentNoteRepository

    constructor(paymentNoteRepository: PaymentNoteRepository){
        this.paymentNoteRepository = paymentNoteRepository
    }

    generatePaymentNote(classroom: Classroom, ){
        const allClassRoomPayments:PaymentNote[] = []
        
        classroom.students.map((student, index) => {
            const newPaymentNote = new PaymentNote(index, student.bi, classroom.id, 5000, Date.now().toString())
            
            allClassRoomPayments.push(newPaymentNote)

            eventBus.publish("paymentNoteGenerated", newPaymentNote)
        }) 

        this.paymentNoteRepository.savePaymentNote(allClassRoomPayments)
    }
}


export class NotifyStudentService {
    notify(classroom: Classroom){
        classroom.students.map(student => {
            student.notify()
        })
    }
}

export class ClassroomRepository {
    classRooms: Classroom[] = []

    saveClassroom(classRoom: Classroom){
        this.classRooms.push(classRoom)
    }

    getClassroom(): Classroom[] {
        return this.classRooms
    }
}

export class PaymentNoteRepository {
    paymentNotes: PaymentNote[][] = []
    
    savePaymentNote(newPaymentNotes: PaymentNote[]){
        this.paymentNotes.push(newPaymentNotes)
    }
    
    getPaymentNotes(): PaymentNote[][]{
        return this.paymentNotes
    }
}

export class WaitingListRepository {
    students: Student[] = []
   

    saveStudent(student: Student){
        this.students.push(student)

        return this.students
    }

    getStudents(): Student[]{
        return this.students
    }

    clear(){
        this.students = []
    }
}

export class Student {
    bi: string
    name: string
    age: number
    isNotified: boolean = false
  
    constructor(bi: string, name: string, age: number){
        this.bi = bi
        this.name = name
        this.age = age
    }
  
    notify(){
        this.isNotified = true
    }
  }