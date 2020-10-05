import React, { createContext, useContext } from 'react'
import { createMuiTheme, ThemeProvider } from '@material-ui/core'

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

export const RtlContext = createContext(TextDirection.LTR)

interface RtlProviderProps {
  children: React.ReactNodeArray
}

export const RtlProvider = ({ children }: RtlProviderProps) => {
  const direction = useContext(RtlContext)
  const theme = themeWithDirection(direction)

  return (
    <ThemeProvider theme={theme}>
      {children}
    </ThemeProvider>
  )
}
