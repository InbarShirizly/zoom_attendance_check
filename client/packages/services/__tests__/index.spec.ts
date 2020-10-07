import { createTestkit } from './testkit'
import { createServiceClient } from '../src/index'

const baseUrl = 'http://example.com'

describe('Service tests', () => {
  const testkit = createTestkit({ baseUrl })
  const service = createServiceClient({ baseUrl })

  it('should return a classroom by id', async () => {
    const someClassroom = {
      id: 1,
      name: 'Some Class',
      students: []
    }

    testkit.addClassroom(someClassroom)

    const classroom = await service.getClassroomById(someClassroom.id)
    expect(classroom).toEqual(someClassroom)
  })

  it('should return all classrooms', async () => {
    const someClassroom = {
      id: 1,
      name: 'Some Class',
      students: []
    }

    testkit.addClassroom(someClassroom)

    const classrooms = await service.getClassrooms()
    expect(classrooms).toHaveLength(1)
    expect(classrooms[0]).toEqual({ id: someClassroom.id, name: someClassroom.name })
  })
})
