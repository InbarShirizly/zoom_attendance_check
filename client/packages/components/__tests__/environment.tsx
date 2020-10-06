import React, { ReactNode, ReactNodeArray } from 'react'
import { render, unmountComponentAtNode } from 'react-dom'
import { ErrorBoundary } from './error-boundary'

export const createTestEnvironment = () => {
  let errors: Error[] = []
  let container: HTMLDivElement | null = null

  const beforeAndAfter = () => {
    beforeAll(() => {
      container = document.createElement('div')
      document.body.appendChild(container)
    })

    afterAll(() => {
      if (container !== null) {
        unmountComponentAtNode(container)
        container.remove()
        container = null
      }

      errors = []
    })
  }

  const getContainer = () => container

  const getErrors = () => errors

  const renderInContainer = (component: ReactNode | ReactNodeArray) =>
    render(
      <>{component}</>,
      container
    )

  const renderInErrorBoundary = (component: ReactNode | ReactNodeArray) =>
    renderInContainer(
      <ErrorBoundary onError={err => errors.push(err)}>
        {component}
      </ErrorBoundary>
    )

  return {
    getContainer,
    getErrors,
    beforeAndAfter,
    renderInErrorBoundary,
    render: renderInContainer
  }
}
