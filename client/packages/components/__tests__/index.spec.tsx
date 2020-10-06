import React from 'react'
import { act } from 'react-dom/test-utils'
import { createTestEnvironment } from './environment'
import { createProvider } from '../src/providers/create-provider'

describe('Provider utility tests', () => {
  const env = createTestEnvironment()

  env.beforeAndAfter()

  it('should create a provider with the correct display name', async () => {
    const container = env.getContainer()
    const resourceName = 'SomeResource'
    const { Provider } = createProvider(resourceName, () => 0, 0)

    act(() => {
      env.render(
        <Provider>
          abcd
        </Provider>
      )
    })

    expect(Provider.displayName).toEqual(`${resourceName}Provider`)
    expect(container?.textContent).toEqual('abcd')
  })

  it('should report an error if the useProvider hook is used outside of the provider', async () => {
    const resourceName = 'SomeResource'
    const { useProvider } = createProvider(resourceName, () => 0, 0)

    const Component = () => {
      const [state] = useProvider()
      return <h1>{state}</h1>
    }

    act(() => {
      env.renderInErrorBoundary(
        <Component />
      )
    })

    const [err] = env.getErrors()
    expect(err.message).toEqual(`use${resourceName} must be used within a ${resourceName}Provider`)
  })
})
