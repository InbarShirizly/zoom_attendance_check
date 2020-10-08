import { Service, ShallowClassroom } from 'services'
import { ClassroomsThunk } from '../providers/ClassroomsProvider'

export const createClassroomActions = (service: Service) => {
  const fetchAll = (): ClassroomsThunk => async dispatch => {
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

  const select = (id: number): ClassroomsThunk => async dispatch => {
    dispatch({ type: 'SELECT_CLASSROOM_START' })
    try {
      const classroom = await service.getClassroomById(id)
      return dispatch({
        type: 'SELECT_CLASSROOM_SUCESS',
        selectedClassroom: classroom
      })
    } catch (e) {
      return dispatch({
        type: 'FETCH_ERROR',
        error: e
      })
    }
  }

  return {
    fetchAll,
    create,
    select
  }
}
