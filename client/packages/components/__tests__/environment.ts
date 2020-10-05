import { unmountComponentAtNode } from 'react-dom'

export const createTestEnvironment = () => {
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
    })
  }

  const getContainer = () => container

  return {
    getContainer,
    beforeAndAfter
  }
}
