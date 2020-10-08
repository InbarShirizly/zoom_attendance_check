import React, {
  createContext,
  ReactNode,
  ReactNodeArray,
  Dispatch,
  useCallback,
  useContext,
  useState,
  useRef
} from 'react'

export type ThunkedDispatch<State, Action> = Dispatch<Action | Thunk<State, Action>>
export type Thunk<State, Action> = (dispatch: ThunkedDispatch<State, Action>, getState: () => State) => void
type Reducer<State, Action> = (state: State, action: Action) => State

export const useThunkedReducer = <State, Action>(reducer: Reducer<State, Action>, initialState: State): [State, ThunkedDispatch<State, Action>] => {
  const [internalState, setInternalState] = useState(initialState)

  const state = useRef(internalState)
  const getState = useCallback(() => state.current, [state])
  const setState = useCallback((newState: State) => {
    state.current = newState
    setInternalState(newState)
  }, [state, setInternalState])

  const reduce = useCallback((action: Action) => {
    return reducer(getState(), action)
  }, [reducer, getState])

  const dispatch: ThunkedDispatch<State, Action> = useCallback((action: any) => {
    return typeof action === 'function'
      ? action(dispatch, getState)
      : setState(reduce(action))
  }, [getState, setState, reduce])

  return [internalState, dispatch]
}

export interface ProviderProps {
  children: ReactNode | ReactNodeArray
}

export const createProvider = <
  State extends {},
  Action extends { type: any; }
>(resourceName: string, reducer: Reducer<State, Action>, initialState: State) => {
  const StateContext = createContext<State | undefined>(undefined)
  const DispatchContext = createContext<ThunkedDispatch<State, Action> | undefined>(undefined)

  const Provider = ({ children }: ProviderProps) => {
    const [state, dispatch] = useThunkedReducer(reducer, initialState)

    return (
      <StateContext.Provider value={state}>
        <DispatchContext.Provider value={dispatch}>
          {children}
        </DispatchContext.Provider>
      </StateContext.Provider>
    )
  }
  Provider.displayName = `${resourceName}Provider`

  const useProvider = (): [State, ThunkedDispatch<State, Action>] => {
    const state = useContext(StateContext)
    const dispatch = useContext(DispatchContext)

    if (!state || !dispatch) {
      throw new Error(`use${resourceName} must be used within a ${Provider.displayName}`)
    }

    return [state, dispatch]
  }

  return { Provider, useProvider }
}
