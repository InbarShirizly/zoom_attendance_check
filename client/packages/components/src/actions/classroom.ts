import { Service } from 'services'
import { ClassroomsThunk } from '../providers/ClassroomsProvider'

export const createClassroomActions = (service: Service) => {
  const fetch = (): ClassroomsThunk => async dispatch => {
    dispatch({ type: 'FETCH_CLASSROOMS_START' })
    try {
      const classrooms = await service.getClassrooms()
      return dispatch({
        type: 'FETCH_CLASSROOMS_SUCCESS',
        classrooms
      })
    } catch (e) {
      return dispatch({
        type: 'FETCH_ERROR',
        error: e
      })
    }
  }

  const create = (name: string, studentsFile: File): ClassroomsThunk => async dispatch => {
    dispatch({ type: 'CREATE_CLASSROOM_START' })
    try {
      const classroom = await service.createClassroom(name, studentsFile)
      return dispatch({
        type: 'CREATE_CLASSROOM_SUCCESS',
        classroom
      })
    } catch (e) {
      return dispatch({
        type: 'FETCH_ERROR',
        error: e
      })
    }
  }

  return {
    fetch,
    create
  }
}
