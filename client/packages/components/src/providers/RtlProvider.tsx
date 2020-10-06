import React from 'react'
import { createMuiTheme, jssPreset, StylesProvider, ThemeProvider } from '@material-ui/core'
import { create as createJss } from 'jss'
import jssRtl from 'jss-rtl'
import { createProvider } from './create-provider'

export enum TextDirection {
  RTL = 'rtl',
  LTR = 'ltr'
}

const themeWithDirection = (direction: TextDirection) => createMuiTheme({
  typography: {
    fontFamily: '"Heebo", "HelveticaNeue-Light", "Helvetica Neue Light", "Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif'
  },
  direction
})

type Action = { type: 'SET_RTL' } | { type: 'SET_LTR' }

interface RtlProviderProps {
  children: React.ReactNodeArray | React.ReactNode
}

const rtlReducer = (state: TextDirection, action: Action) => {
  switch (action.type) {
    case 'SET_LTR':
      return TextDirection.LTR
    case 'SET_RTL':
      return TextDirection.RTL
    default:
      return state
  }
}

const {
  Provider: TextDirectionProvider,
  useProvider: useTextDirection
} = createProvider('TextDirection', rtlReducer, TextDirection.LTR)

const jss = createJss({ plugins: [...jssPreset().plugins, jssRtl()] })

const RtlStylesProvider = ({ children }: RtlProviderProps) => {
  const [state] = useTextDirection()
  const theme = themeWithDirection(state)

  // TODO - Check for best practices. This will happen on every render probably.
  document.body.dir = state

  return (
    <StylesProvider jss={jss}>
      <ThemeProvider theme={theme}>
        {children}
      </ThemeProvider>
    </StylesProvider>
  )
}

const RtlProvider = ({ children }: RtlProviderProps) => (
  <TextDirectionProvider>
    <RtlStylesProvider>
      {children}
    </RtlStylesProvider>
  </TextDirectionProvider>
)

export { RtlProvider, useTextDirection }
