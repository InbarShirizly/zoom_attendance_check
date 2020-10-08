import ky from 'ky-universal'

export interface StudentData {
  id: number
  orgClass: string

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

export type ShallowClassroom = Pick<Classroom, 'id' | 'name'>

export interface AuthResponse {
  token: string
}

export interface ClientOptions {
  baseUrl: string
  token?: string
}

const apiStudentToApp = (json: Record<string, any>): StudentData => ({
  id: json.id,
  name: json.name,
  orgClass: json.org_class,
  phone: json.phone ?? undefined,
  idNumber: json.id_number ?? undefined
})

export const createServiceClient = ({ baseUrl, token }: ClientOptions) => {
  const headers = token
    ? { Authorization: `Bearer ${token}` }
    : {}

  const httpClient = ky.extend({
    prefixUrl: baseUrl,
    headers
  })

  const register = (username: string, email: string, password: string) =>
    httpClient.post('api/register', {
      json: {
        username,
        email,
        password
      }
    }).json<AuthResponse>()

  const login = (username: string, password: string) =>
    httpClient.post('api/login', {
      json: {
        auth: username,
        password
      }
    }).json<AuthResponse>()

  const getClassrooms = () => httpClient.get('api/classrooms').json<ShallowClassroom[]>()

  const getClassroomById = (id: number): Promise<Classroom> => httpClient.get(`api/classrooms/${id}`)
    .then(res => res.json())
    .then(json => ({
      ...json,
      students: json.students.map((s: Record<string, any>) => apiStudentToApp(s))
    }))

  const createClassroom = (name: string, file: File) => {
    const data = new FormData()
    data.append('name', name)
    data.append('students_file', file)

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
    login,
    register,
    getClassrooms,
    createClassroom,
    deleteClassroom,
    getClassroomById,
    deleteAllClassrooms,
    changeClassroomName
  }
}

export type Service = ReturnType<typeof createServiceClient>
