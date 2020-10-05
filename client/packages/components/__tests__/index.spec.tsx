import { createTestEnvironment } from './environment'

describe('tests', () => {
  const env = createTestEnvironment()

  env.beforeAndAfter()

  it('should mount', async () => {
    const wrapper = env.mount()
  })
})
