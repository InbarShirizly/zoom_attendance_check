import { createMuiTheme, ThemeProvider } from '@material-ui/core'
import React from 'react'

const theme = createMuiTheme({
  typography: {
    fontFamily: '"Heebo", "HelveticaNeue-Light", "Helvetica Neue Light", "Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif'
  },
  direction: 'rtl'
})

interface RtlProviderProps {
  children: React.ReactNodeArray
}

export const RtlProvider = ({ children }: RtlProviderProps) => {
  return (
    <ThemeProvider theme={theme}>
      {children}
    </ThemeProvider>
  )
}
