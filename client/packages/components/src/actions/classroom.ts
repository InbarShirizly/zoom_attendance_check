import { Service } from 'services'
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

  /**
   * Makes a request to create a report in the database with a file to parse
   * @returns A report object, the parsed file data
   */
  const createReport = (
    classId: number,
    file: File,
    timeDelta: number,
    firstSentence: string,
    excludedUsers: string,
    description: string
  ): ClassroomsThunk => async dispatch => {
    dispatch({ type: 'CREATE_REPORT_START' })
    try {
      const { id: reportId } = await service.createReport(classId, file, timeDelta, firstSentence, excludedUsers, description)
      const report = await service.getReport(classId, reportId)
      return dispatch({
        type: 'CREATE_REPORT_SUCCESS',
        report
      })
    } catch (error) {
      return dispatch({
        type: 'FETCH_ERROR',
        error
      })
    }
  }

  return {
    fetchAll,
    create,
    select,
    createReport
  }
}
