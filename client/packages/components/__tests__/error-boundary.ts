import { Component, ReactNode, ReactNodeArray } from 'react'

interface ErrorBoundaryState {
  failed: boolean
}

interface ErrorBoundaryProps {
  children: ReactNode | ReactNodeArray
  onError<T extends Error>(error: T): void
}

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor (props: ErrorBoundaryProps) {
    super(props)

    this.state = { failed: false }
  }

  static getDerivedStateFromError () {
    return { failed: true }
  }

  componentDidCatch<T extends Error> (error: T) {
    this.props.onError(error)
  }

  render () {
    if (this.state.failed) return null
    return this.props.children
  }
}
