import { Classroom, ShallowClassroom } from 'services'
import { createProvider, Thunk } from './create-provider'

interface ClassroomsState {
  classrooms: ShallowClassroom[]
  selectedClassroom?: Classroom
}

type FetchAction = {
  type: 'FETCH_CLASSROOMS_START'
}

type SuccessfulFetchAction = {
  type: 'FETCH_CLASSROOMS_SUCCESS',
  classrooms: ShallowClassroom[]
}

type ErrorAction = {
  type: 'FETCH_ERROR',
  error?: Error
}

type CreateAction = {
  type: 'CREATE_CLASSROOM_START'
}

type SuccessfulCreateAction = {
  type: 'CREATE_CLASSROOM_SUCCESS',
  classroom: Classroom
}

type SelectAction = {
  type: 'SELECT_CLASSROOM_START'
}

type SuccesfulSelectAction = {
  type: 'SELECT_CLASSROOM_SUCESS',
  selectedClassroom: Classroom
}

type Action =
  | FetchAction | SuccessfulFetchAction
  | CreateAction | SuccessfulCreateAction
  | SelectAction | SuccesfulSelectAction
  | ErrorAction

const classroomsReducer = (state: ClassroomsState, action: Action) => {
  switch (action.type) {
    case 'FETCH_CLASSROOMS_SUCCESS':
      return { ...state, classrooms: action.classrooms }
    case 'CREATE_CLASSROOM_SUCCESS':
      return {
        ...state,
        classrooms: [
          ...state.classrooms,
          { id: action.classroom.id, name: action.classroom.name }
        ],
        selectedClassroom: action.classroom
      }
    case 'FETCH_ERROR':
      return { ...state, classrooms: [] }
    default:
      return state
  }
}

export type ClassroomsThunk = Thunk<ClassroomsState, Action>

const {
  Provider: ClassroomsProvider,
  useProvider: useClassrooms
} = createProvider('Classrooms', classroomsReducer, { classrooms: [] })

export { ClassroomsProvider, useClassrooms }
