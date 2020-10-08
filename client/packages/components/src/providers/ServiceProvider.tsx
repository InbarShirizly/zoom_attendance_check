import { createServiceClient, Service } from 'services'
import { createProvider } from './create-provider'

const BASE_URL = 'http://localhost:5000'

const service = createServiceClient({ baseUrl: BASE_URL })

type Action = {
  type: 'SET_TOKEN',
  token?: string
}

const reducer = (state: Service, action: Action) => {
  switch (action.type) {
    case 'SET_TOKEN':
      return action.token
        ? createServiceClient({ baseUrl: BASE_URL, token: action.token })
        : state
    default:
      return state
  }
}

const {
  Provider: ServiceProvider,
  useProvider: useService
} = createProvider('Service', reducer, service)

export { ServiceProvider, useService }
