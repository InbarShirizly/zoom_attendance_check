import nock from 'nock'
import { Classroom } from '../src/index'

interface TestkitOptions {
  baseUrl: string
}

const parseNum = (str?: string) => {
  if (!str) return undefined
  const num = parseInt(str, 10)
  return isNaN(num) ? undefined : num
}

const createDataManager = () => {
  const classrooms = new Map<number, Classroom>()

  return {
    getClassrooms: () => Array.from(classrooms.values()),
    getClassroomById: (id: number) => classrooms.get(id),
    addClassroom: (classroom: Classroom) => classrooms.set(classroom.id, classroom),
    removeClassroomById: (id: number) => classrooms.delete(id),
    clasroomExistsById: (id: number) => classrooms.has(id),
    updateClassroomNameById: (id: number, newName: string) => {
      const classroom = classrooms.get(id)
      classroom.name = newName
    }
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
    .get(classroomByIdRegex)
    .reply(uri => {
      const id = parseNum(classroomByIdRegex.exec(uri).groups.id)

      if (!id) return [400, {}]
      if (!dataManager.clasroomExistsById(id)) return [404, {}]

      return [200, dataManager.getClassroomById(id)]
    })
    .put(classroomByIdRegex)
    .reply((uri, body: Record<string, any>) => {
      const id = parseNum(classroomByIdRegex.exec(uri).groups.id)

      if (!id) return [400, {}]
      if (!dataManager.clasroomExistsById(id)) return [404, {}]

      dataManager.updateClassroomNameById(id, body.new_name)

      return [204]
    })
}

export const createTestkit = ({ baseUrl }: TestkitOptions) => {
  const nockInstance = nock(baseUrl).persist()
  const dataManager = createDataManager()

  patchClassroomRoutes(nockInstance, dataManager)

  return dataManager
}
