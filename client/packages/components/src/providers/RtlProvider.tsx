import React, { createContext, useContext, useReducer } from 'react'
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

type Action = { type: 'SET_RTL' } | { type: 'SET_LTR' }
type Dispatch = (action: Action) => void

const RtlStateContext = createContext<TextDirection | undefined>(undefined)
const RtlDispatchContext = createContext<Dispatch | undefined>(undefined)

interface RtlProviderProps {
  children: React.ReactNodeArray
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

export const RtlProvider = ({ children }: RtlProviderProps) => {
  const [state, dispatch] = useReducer(rtlReducer, TextDirection.LTR)
  const theme = themeWithDirection(state)

  return (
    <ThemeProvider theme={theme}>
      <RtlStateContext.Provider value={state}>
        <RtlDispatchContext.Provider value={dispatch}>
          {children}
        </RtlDispatchContext.Provider>
      </RtlStateContext.Provider>
    </ThemeProvider>
  )
}

export const useRtlContext = () => {
  const state = useContext(RtlStateContext)
  const dispatch = useContext(RtlDispatchContext)

  if (!state || !dispatch) {
    throw new Error('useRtlContext must be used within a RtlProvider')
  }

  return { state, dispatch }
}
