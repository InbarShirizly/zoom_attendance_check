import React from 'react'
import { render } from 'react-dom'
import { act } from 'react-dom/test-utils'
import { createTestEnvironment } from './environment'

const Component = () => <h1>Hello, world!</h1>

describe('tests', () => {
  const env = createTestEnvironment()

  env.beforeAndAfter()

  it('should mount', async () => {
    const container = env.getContainer()

    act(() => {
      render(
        <Component />,
        container
      )
    })

    expect(container.querySelector('h1')?.textContent).toEqual('Hello, world!')
  })
})
