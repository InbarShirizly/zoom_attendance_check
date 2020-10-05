import { createMount, createRender, createShallow } from '@material-ui/core/test-utils'

export const createTestEnvironment = () => {
  let mount: ReturnType<typeof createMount>
  let render: ReturnType<typeof createRender>
  let shallow: ReturnType<typeof createShallow>

  const beforeAndAfter = () => {
    beforeEach(() => {
      mount = createMount()
      render = createRender()
      shallow = createShallow()
    })

    afterEach(() => {
      mount.cleanUp()
    })
  }

  return {
    mount,
    render,
    shallow,
    beforeAndAfter
  }
}
