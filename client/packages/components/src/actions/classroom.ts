import { Service } from 'services'
import { ClassroomsThunk } from '../providers/ClassroomsProvider'

export const createClassroomActions = (service: Service, token?: string) => {
  const fetch = (): ClassroomsThunk => async dispatch => {
    dispatch({ type: 'FETCH_CLASSROOMS_START' })
    try {
      const classrooms = await service.getClassrooms()
      dispatch({
        type: 'FETCH_CLASSROOMS_SUCCESS',
        classrooms
      })
    } catch (e) {
      dispatch({
        type: 'FETCH_ERROR',
        error: e
      })
    }
  }

  return {
    fetch
  }
}
