import React from 'react'
import { act, Simulate } from 'react-dom/test-utils'
import { createTestEnvironment } from '../environment'
import { CustomAppBar } from '../../src/layout/AppBar'
import { RtlProvider, TextDirection, useTextDirection } from '../../src/providers'

describe('AppBar', () => {
  const env = createTestEnvironment()

  env.beforeAndAfter()

  it('should render in an RtlProvider', async () => {
    act(() => {
      env.render(
        <RtlProvider>
          <CustomAppBar i18n={{ changeLanguage: _ => _ }} t={_ => _} />
        </RtlProvider>
      )
    })

    expect(document.querySelector('[data-testid="appbar"]')).not.toBeNull()
  })

  it('should render with translations', async () => {
    const appTitle = 'app'

    act(() => {
      env.render(
        <RtlProvider>
          <CustomAppBar i18n={{ changeLanguage: _ => _ }} t={key => key === 'app_title' ? appTitle : key} />
        </RtlProvider>
      )
    })

    const appTitleEl = document.querySelector('[data-testid="app-title"]')!
    expect(appTitleEl.textContent).toEqual(appTitle)
  })

  describe('Language menu', () => {
    it('should call i18n changeLanguage method', async () => {
      const changeLanguage = jest.fn()

      act(() => {
        env.render(
          <RtlProvider>
            <CustomAppBar i18n={{ changeLanguage }} t={_ => _} />
          </RtlProvider>
        )
      })

      const menu = document.querySelector('[data-testid="language-menu"]')!
      Simulate.click(menu)

      const hebButton = document.querySelector('[data-testid="hebrew-button"]')!
      Simulate.click(hebButton)

      expect(changeLanguage).toHaveBeenCalledWith('he')
    })

    it('should change text direction status', async () => {
      const DummyComponent = () => <div data-testid='dummy'>{useTextDirection()[0]}</div>

      act(() => {
        env.render(
          <RtlProvider>
            <CustomAppBar i18n={{ changeLanguage: _ => _ }} t={_ => _} />
            <DummyComponent />
          </RtlProvider>
        )
      })

      const menu = document.querySelector('[data-testid="language-menu"]')!
      Simulate.click(menu)

      const hebButton = document.querySelector('[data-testid="hebrew-button"]')!
      Simulate.click(hebButton)

      const dummy = document.querySelector('[data-testid="dummy"]')!
      expect(dummy.textContent).toEqual(TextDirection.RTL)
    })
  })
})
