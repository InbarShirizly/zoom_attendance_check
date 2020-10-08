import React, {
  createContext,
  ReactNode,
  ReactNodeArray,
  Dispatch as ReactDispatch,
  useCallback,
  useContext,
  useReducer
} from 'react'

type ActionCreator<State, Action> = (dispatch: ReactDispatch<Action>, state: State) => PromiseLike<Action>
type Dispatch<State, Action> = (action: Action | ActionCreator<State, Action>) => void
type Reducer<State, Action> = (state: State, action: Action) => State

export interface ProviderProps {
  children: ReactNode | ReactNodeArray
}

export const createProvider = <
  State extends {},
  Action extends { type: any; }
>(resourceName: string, reducer: Reducer<State, Action>, initialState: State) => {
  const StateContext = createContext<State | undefined>(undefined)
  const DispatchContext = createContext<Dispatch<State, Action> | undefined>(undefined)

  const Provider = ({ children }: ProviderProps) => {
    const [state, dispatch] = useReducer(reducer, initialState)

    const customDispatch = useCallback(async (action: Action | ActionCreator<State, Action>) => {
      if (typeof action === 'function') {
        const newAction = await action(dispatch, state)
        return dispatch(newAction)
      }

      return dispatch(action)
    }, [])

    return (
      <StateContext.Provider value={state}>
        <DispatchContext.Provider value={customDispatch}>
          {children}
        </DispatchContext.Provider>
      </StateContext.Provider>
    )
  }
  Provider.displayName = `${resourceName}Provider`

  const useProvider = (): [State, Dispatch<State, Action>] => {
    const state = useContext(StateContext)
    const dispatch = useContext(DispatchContext)

    if (!state || !dispatch) {
      throw new Error(`use${resourceName} must be used within a ${Provider.displayName}`)
    }

    return [state, dispatch]
  }

  return { Provider, useProvider }
}
