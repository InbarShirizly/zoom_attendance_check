import React, {
  createContext,
  ReactNode,
  ReactNodeArray,
  useContext,
  useReducer
} from 'react'

type Dispatch<Action> = (action: Action) => void
type Reducer<State, Action> = (state: State, action: Action) => State

export interface ProviderProps {
  children: ReactNode | ReactNodeArray
}

export const createProvider = <
  State extends {},
  Action extends { type: any; }
>(resourceName: string, reducer: Reducer<State, Action>, initialState: State) => {
  const StateContext = createContext<State | undefined>(undefined)
  const DispatchContext = createContext<Dispatch<Action> | undefined>(undefined)

  const Provider = ({ children }: ProviderProps) => {
    const [state, dispatch] = useReducer(reducer, initialState)

    return (
      <StateContext.Provider value={state}>
        <DispatchContext.Provider value={dispatch}>
          {children}
        </DispatchContext.Provider>
      </StateContext.Provider>
    )
  }
  Provider.displayName = `${resourceName}Provider`

  const useProvider = (): [State, Dispatch<Action>] => {
    const state = useContext(StateContext)
    const dispatch = useContext(DispatchContext)

    if (!state || !dispatch) {
      throw new Error(`use${resourceName} must be used within a ${Provider.displayName}`)
    }

    return [state, dispatch]
  }

  return { Provider, useProvider }
}
