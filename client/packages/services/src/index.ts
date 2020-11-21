import ky from 'ky-universal'

export interface StudentData {
  id: number
  orgClass: string

  name?: string
  phone?: number
  idNumber?: string
}

/** Possible statuses for student attendance in a class. */
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

/**
 * The student and their attendance status in the report.
 */
export interface StudentStatus {
  studentId: number
  status: Attendance
  studentName: string
}

/**
 * The information stored for a report.
 */
export interface Report {
  id: number
  classId: number
  description: string
  timestamp: number
  studentStatuses: StudentStatus[]
}

export type ShallowReport = Pick<Report, 'id' | 'description' | 'timestamp'>

export interface ReportsServerResponse {
  id: number,
  description: string,
  time: number
}

const apiReportsToApp = (reports: ReportsServerResponse[]): ShallowReport[] =>
  reports.map(({ id, description, time }): ShallowReport => ({
    id,
    description,
    timestamp: time
  }))

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

/** Convert the server response to an object with camel casing. */
const apiReportToApp = (id: number, json: Record<string, any>): Report => ({
  id,
  classId: json.class_id,
  timestamp: json.timestamp,
  description: json.description,
  studentStatuses: json.student_statuses.map((status: Record<string, any>) => ({
    status: status.status,
    studentName: status.student_name,
    studentId: status.student_id
  }))
})

export const createServiceClient = ({ baseUrl, token }: ClientOptions) => {
  const headers = token ? { Authorization: `Bearer ${token}` } : {}

  const httpClient = ky.extend({
    prefixUrl: baseUrl,
    headers
  })

  const register = (username: string, email: string, password: string) =>
    httpClient
      .post('api/register', {
        json: {
          username,
          email,
          password
        }
      })
      .json<AuthResponse>()

  const login = (username: string, password: string) =>
    httpClient
      .post('api/login', {
        json: {
          auth: username,
          password
        }
      })
      .json<AuthResponse>()

  const getClassrooms = () => httpClient.get('api/classrooms').json<ShallowClassroom[]>()

  const getClassroomById = (id: number): Promise<Classroom> =>
    httpClient
      .get(`api/classrooms/${id}`)
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

  const changeClassroomName = (id: number, newName: string) =>
    httpClient.put(`api/classrooms/${id}`, {
      json: {
        new_name: newName
      }
    })

  const deleteClassroom = (id: number) => httpClient.delete(`api/classrooms/${id}`).json()

  const deleteAllClassrooms = () => httpClient.delete('api/classrooms').json()

  /**
   * Sends a request to the server with the specified parameters to create a report.
   */
  const createReport = (
    id: number,
    file: File,
    timeDelta: number,
    firstSentence: string,
    excludedUsers: string,
    description: string
  ) => {
    const data = new FormData()
    data.append('chat_file', file)
    data.append('time_delta', timeDelta.toString())
    data.append('first_sentence', firstSentence)
    data.append('not_included_zoom_users', excludedUsers)
    data.append('description', description)
    return httpClient.post(`api/classrooms/${id}/reports`, { body: data }).json<Report>()
  }

  /**
   * Retrieve a specific report by its id.
   */
  const getReport = async (classId: number, reportId: number): Promise<Report> => {
    const res = await httpClient.get(`api/classrooms/${classId}/reports/${reportId}`).json<Record <string, any>>()
    return apiReportToApp(reportId, res)
  }

  /**
   * Fetches all reports for a specific class.
   */
  const getAllClassReports = async (classId: number): Promise<ShallowReport[]> =>
    httpClient.get(`/api/classrooms/${classId}/reports`)
      .json<ReportsServerResponse[]>()
      .then(apiReportsToApp)

  return {
    login,
    register,
    getClassrooms,
    createClassroom,
    deleteClassroom,
    getClassroomById,
    deleteAllClassrooms,
    changeClassroomName,
    createReport,
    getReport,
    getAllClassReports
  }
}

export type Service = ReturnType<typeof createServiceClient>
