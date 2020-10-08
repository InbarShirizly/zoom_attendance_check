import { createProvider, Thunk } from './create-provider'

interface AuthState {
  token?: string
  failed: boolean
  faliureReason?: string
}

type LoginAction = {
  type: 'LOGIN',
  username: string,
  password: string
}

type RegisterAction = {
  type: 'REGISTER',
  username: string,
  password: string,
  confirmPasword: string,
  email: string
}

type LogoutAction = {
  type: 'LOGOUT'
}

type SuccessAction = {
  type: 'AUTH_SUCCESS',
  token: string
}

type FailAction = {
  type: 'AUTH_FAILED'
  error?: Error
}

type Action = LoginAction | LogoutAction | SuccessAction | FailAction | RegisterAction

const authReducer = (state: AuthState, action: Action) => {
  switch (action.type) {
    case 'AUTH_SUCCESS':
      return { ...state, token: action.token, failed: false }
    case 'AUTH_FAILED':
      return { ...state, failed: true, failureReason: action.error?.message }
    case 'LOGOUT':
      return { failed: false }
    case 'REGISTER':
      return action.password !== action.confirmPasword
        ? { ...state, failed: true, failureReason: 'password_mismatch' }
        : state
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
