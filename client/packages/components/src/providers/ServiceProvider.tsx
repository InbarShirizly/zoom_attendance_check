import { createServiceClient, Service } from 'services'
import { createProvider } from './create-provider'

const BASE_URL = 'http://localhost:5000'

const service = createServiceClient({
  baseUrl: BASE_URL,
  token: window.sessionStorage.getItem('token') ?? undefined
})

type SetTokenAction = {
  type: 'SET_TOKEN',
  token?: string
}

type UnsetTokenAction = {
  type: 'UNSET_TOKEN'
}

type Action = SetTokenAction | UnsetTokenAction

const reducer = (state: Service, action: Action) => {
  switch (action.type) {
    case 'SET_TOKEN':
      return action.token
        ? createServiceClient({ baseUrl: BASE_URL, token: action.token })
        : state
    case 'UNSET_TOKEN':
      return createServiceClient({ baseUrl: BASE_URL })
    default:
      return state
  }
}

const {
  Provider: ServiceProvider,
  useProvider: useService
} = createProvider('Service', reducer, service)

export { ServiceProvider, useService }
