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
  const httpClient = ky.extend({
    prefixUrl: baseUrl
  })

  const getClassrooms = () => httpClient.get('api/classrooms').json<ShallowClassroom[]>()

  const getClassroomById = (id: number) => httpClient.get(`api/classrooms/${id}`).json<Classroom>()

  const createClassroom = (name: string, file: File) => {}

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
