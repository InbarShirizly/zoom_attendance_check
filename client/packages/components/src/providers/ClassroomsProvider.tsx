import { Classroom } from 'services'
import { createProvider, Thunk } from './create-provider'

interface ClassroomsState {
  classrooms: Classroom[]
}

type FetchAction = {
  type: 'FETCH_CLASSROOMS',
  token: string
}

type Action = FetchAction

const classroomsReducer = (state: ClassroomsState, action: Action) => {
  switch (action.type) {
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
