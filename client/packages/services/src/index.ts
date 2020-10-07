import ky from 'ky-universal'

export interface StudentData {
  id: number
  classId: number

  name?: string
  phone?: number
  idNumber?: string
}

export enum Attendance {
  Absent = 0,
  Partial = 1,
  Attended = 2
}

export interface Classroom {
  name: string
  id: number
  students: StudentData[]
}

type ShallowClassroom = Pick<Classroom, 'id' | 'name'>

interface ClientOptions {
  baseUrl: string
}

export const createServiceClient = ({ baseUrl }: ClientOptions) => {
  const getClassrooms = () => {}

  const getClassroomById = (id: number) => {}

  const createClassroom = (classroom: Classroom) => {}

  const changeClassroom = (id: number, newName: string) => {}

  const deleteClassroom = (id: number) => {}

  const deleteAllClassrooms = () => {}

  return {
    getClassrooms,
    createClassroom,
    changeClassroom,
    deleteClassroom,
    getClassroomById,
    deleteAllClassrooms
  }
}
