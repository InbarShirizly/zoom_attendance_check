import { createProvider } from './create-provider'

interface AuthState {
  token?: string
  authFailed: boolean
}

type LoginAction = { type: 'LOGIN', usernam: string, password: string }
type LogoutAction = { type: 'LOGOUT' }
type SuccessAction = { type: 'AUTH_SUCCESS', token: string }
type FailAction = { type: 'AUTH_FAILED' }
type Action = LoginAction | LogoutAction | SuccessAction | FailAction

const authReducer = (state: AuthState, action: Action) => {
  switch (action.type) {
    case 'AUTH_SUCCESS':
      return { ...state, token: action.token, authFailed: false }
    case 'AUTH_FAILED':
      return { ...state, authFailed: true }
    case 'LOGOUT':
      return { authFailed: false }
    default:
      return state
  }
}

const {
  Provider: AuthProvider,
  useProvider: useAuth
} = createProvider('Auth', authReducer, { authFailed: false })

export { AuthProvider, useAuth }
