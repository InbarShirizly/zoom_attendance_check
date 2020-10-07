import { createTestkit } from './testkit'
import { createServiceClient } from '../src/index'

const baseUrl = 'http://example.com'

describe('Service tests', () => {
  const testkit = createTestkit({ baseUrl })
  const service = createServiceClient({ baseUrl })

  it('should create a classroom', async () => {
    const someName = 'Some Class'
    const someFile = new File([], 'students-list.xslx', {})

    await service.createClassroom(someName, someFile)

    const classrooms = testkit.getClassrooms()
    expect(classrooms).toHaveLength(1)
    expect(classrooms[0]).toEqual({
      id: expect.any(Number),
      name: someName,
      students: []
    })
  })

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

  it('should delete a classroom by id', async () => {
    const someClassroom = {
      id: 1,
      name: 'Some Class',
      students: []
    }

    testkit.addClassroom(someClassroom)

    await service.deleteClassroom(someClassroom.id)

    expect(testkit.getClassroomById(someClassroom.id)).not.toBeDefined()
  })

  it('should delete all classrooms', async () => {
    const someClassroom = {
      id: 1,
      name: 'Some Class',
      students: []
    }

    testkit.addClassroom(someClassroom)

    await service.deleteAllClassrooms()

    expect(testkit.getClassroomById(someClassroom.id)).not.toBeDefined()
  })

  it("should change a classrom's name", async () => {
    const someClassroom = {
      id: 1,
      name: 'Some Class',
      students: []
    }
    const someName = 'Some New Name'

    testkit.addClassroom(someClassroom)

    await service.changeClassroomName(someClassroom.id, someName)

    expect(testkit.getClassroomById(someClassroom.id).name).toEqual(someName)
  })
})
