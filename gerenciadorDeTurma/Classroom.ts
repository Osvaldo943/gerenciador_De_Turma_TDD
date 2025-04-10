import { Student } from "./service_enrollment.ts";

export interface Classroom {
  id: string;
  students: Student[];
}

