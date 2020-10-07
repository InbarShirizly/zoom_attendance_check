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

  const createClassroom = (name: string, file: File) => {
    const data = new FormData()
    data.append('name', name)
    data.append('student_file', file)

    return httpClient.post('api/classrooms', { body: data }).json<Classroom>()
  }

  const changeClassroomName = (id: number, newName: string) => httpClient.put(`api/classrooms/${id}`, {
    json: {
      new_name: newName
    }
  })

  const deleteClassroom = (id: number) => httpClient.delete(`api/classrooms/${id}`).json()

  const deleteAllClassrooms = () => httpClient.delete('api/classrooms').json()

  return {
    getClassrooms,
    createClassroom,
    deleteClassroom,
    getClassroomById,
    deleteAllClassrooms,
    changeClassroomName
  }
}
