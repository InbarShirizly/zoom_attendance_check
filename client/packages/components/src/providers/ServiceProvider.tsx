import { createServiceClient } from 'services'
import { createProvider } from './create-provider'

const BASE_URL = 'http://localhost:5000'

const service = createServiceClient({ baseUrl: BASE_URL })

const {
  Provider: ServiceProvider,
  useProvider: useService
} = createProvider('Service', _ => _, service)

export { ServiceProvider, useService }
