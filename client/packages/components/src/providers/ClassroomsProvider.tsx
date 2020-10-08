import { ShallowClassroom } from 'services'
import { createProvider, Thunk } from './create-provider'

interface ClassroomsState {
  classrooms: ShallowClassroom[]
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

type Action = FetchAction | SuccessfulFetchAction | ErrorAction

const classroomsReducer = (state: ClassroomsState, action: Action) => {
  switch (action.type) {
    case 'FETCH_CLASSROOMS_SUCCESS':
      return { ...state, classrooms: action.classrooms }
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
} = createProvider('Auth', classroomsReducer, { classrooms: [] })

export { ClassroomsProvider, useClassrooms }
