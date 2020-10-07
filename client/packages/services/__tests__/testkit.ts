import nock from 'nock'
import { Classroom } from '../src/index'

interface TestkitOptions {
  baseUrl: string
}

interface Teacher {
  username: string
  email: string
  password: string
  token: string
}

const parseNum = (str?: string | null) => {
  if (!str) return undefined
  const num = parseInt(str, 10)
  return isNaN(num) ? undefined : num
}

const createDataManager = () => {
  const classrooms = new Map<number, Classroom>()
  const users = new Map<string, Teacher>()

  return {
    getClassrooms: () => Array.from(classrooms.values()),
    getClassroomById: (id: number) => classrooms.get(id),
    addClassroom: (classroom: Classroom) => classrooms.set(classroom.id, classroom),
    removeClassroomById: (id: number) => classrooms.delete(id),
    clasroomExistsById: (id: number) => classrooms.has(id),
    updateClassroomNameById: (id: number, newName: string) => {
      const classroom = classrooms.get(id)
      if (classroom) {
        classroom.name = newName
      }
    },
    clearClassrooms: () => classrooms.clear(),

    addUser: (user: Omit<Teacher, 'token'>) =>
      users.set(user.username, { ...user, token: `${user.username}-${user.password}` }),
    getTokenForUser: (username: string) => users.get(username)?.token,
    userExists: (username: string) => users.has(username)
  }
}

type DataManager = ReturnType<typeof createDataManager>

const patchClassroomRoutes = (nockInstance: nock.Scope, dataManager: DataManager) => {
  const classroomByIdRegex = /\/api\/classrooms\/(?<id>\d*)/

  return nockInstance
    .get('/api/classrooms')
    .reply(() => [
      200,
      dataManager
        .getClassrooms()
        .map(c => ({ id: c.id, name: c.name }))
    ])
    .delete('/api/classrooms')
    .reply(() => {
      dataManager.clearClassrooms()
      return [204]
    })
    .get(classroomByIdRegex)
    .reply(uri => {
      const id = parseNum(classroomByIdRegex.exec(uri)?.groups?.id)

      if (!id) return [400, {}]
      if (!dataManager.clasroomExistsById(id)) return [404, {}]

      return [200, dataManager.getClassroomById(id)]
    })
    .put(classroomByIdRegex)
    .reply((uri, body) => {
      const id = parseNum(classroomByIdRegex.exec(uri)?.groups?.id)

      if (!id) return [400, {}]
      if (!dataManager.clasroomExistsById(id)) return [404, {}]

      dataManager.updateClassroomNameById(id, body.new_name)

      return [204]
    })
    .delete(classroomByIdRegex)
    .reply(uri => {
      const id = parseNum(classroomByIdRegex.exec(uri)?.groups?.id)

      if (!id) return [400, {}]
      if (!dataManager.clasroomExistsById(id)) return [404, {}]

      dataManager.removeClassroomById(id)

      return [204]
    })
}

const patchAuthorizationRoutes = (nockInstance: nock.Scope, dataManager: DataManager) => {
  return nockInstance
    .post('/api/login')
    .reply((_, body) => {
      const { auth, password } = body

      if (!dataManager.userExists(auth)) return [404, {}]

      const token = dataManager.getTokenForUser(auth)
      return token === `${auth}-${password}` ? [200, { token }] : [401, {}]
    })
    .post('/api/register')
    .reply((_, body) => {
      const { username, password, email } = body

      if (dataManager.userExists(username)) return [400, {}]

      dataManager.addUser({ username, password, email })
      return [200, { token: dataManager.getTokenForUser(username) }]
    })
}

export const createTestkit = ({ baseUrl }: TestkitOptions) => {
  const nockInstance = nock(baseUrl).persist()
  const dataManager = createDataManager()

  patchClassroomRoutes(nockInstance, dataManager)
  patchAuthorizationRoutes(nockInstance, dataManager)

  return dataManager
}
