type PaymentNoteStatusType = "Não pago" | "pago";
export class PaymentNote {
  id: number;
  idStudent: string;
  idClassroom: string;
  price: number;
  dueDate: string;
  status: PaymentNoteStatusType;

  constructor(
    id: number,
    idStudent: string,
    idClassroom: string,
    price: number,
    dueDate: string,
    status: PaymentNoteStatusType = "Não pago"
  ) {
    this.id = id;
    this.idStudent = idStudent;
    this.idClassroom = idClassroom;
    this.price = price;
    this.dueDate = dueDate;
    this.status = status;
  }
}
