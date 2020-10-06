import React from 'react'
import { act, Simulate } from 'react-dom/test-utils'
import { createTestEnvironment } from '../environment'
import {
  RtlProvider,
  useTextDirection,
  TextDirection
} from '../../src/providers'

describe('RtlProvider', () => {
  const env = createTestEnvironment()

  env.beforeAndAfter()

  describe('DOM manipulation', () => {
    it('should set the body "dir" attribute to ltr by default', async () => {
      const Component = () => (
        <RtlProvider>
          <div />
        </RtlProvider>
      )

      act(() => {
        env.render(
          <Component />
        )
      })

      expect(document.body.dir).toEqual(TextDirection.LTR)
    })

    it('should change the body "dir" attribute on dispatch', async () => {
      const Component = () => {
        const dispatch = useTextDirection()[1]
        const handleClick = () => dispatch({ type: 'SET_RTL' })

        return (
          <button onClick={handleClick} data-testid='button'>
            abcd
          </button>
        )
      }

      act(() => {
        env.render(
          <RtlProvider>
            <Component />
          </RtlProvider>
        )
      })

      const button = document.querySelector('[data-testid="button"]')
      Simulate.click(button)
      expect(document.body.dir).toEqual(TextDirection.RTL)
    })
  })
})
