import { createProvider, Thunk } from './create-provider'

interface AuthState {
  token?: string
  failed: boolean
}

type LoginAction = { type: 'LOGIN', usernam: string, password: string }
type LogoutAction = { type: 'LOGOUT' }
type SuccessAction = { type: 'AUTH_SUCCESS', token: string }
type FailAction = { type: 'AUTH_FAILED' }
type Action = LoginAction | LogoutAction | SuccessAction | FailAction

const authReducer = (state: AuthState, action: Action) => {
  switch (action.type) {
    case 'AUTH_SUCCESS':
      return { ...state, token: action.token, failed: false }
    case 'AUTH_FAILED':
      return { ...state, failed: true }
    case 'LOGOUT':
      return { failed: false }
    default:
      return state
  }
}

export type AuthThunk = Thunk<AuthState, Action>

const {
  Provider: AuthProvider,
  useProvider: useAuth
} = createProvider('Auth', authReducer, { failed: false })

export { AuthProvider, useAuth }
