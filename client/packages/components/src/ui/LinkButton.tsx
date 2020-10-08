import React from 'react'
import { RouteComponentProps, withRouter } from 'react-router-dom'
import { Button, ButtonProps } from '@material-ui/core'

interface LinkButtonProps extends RouteComponentProps, ButtonProps {
  to: string
}

const LinkButtonComp = ({ children, history, to, ...otherProps }: LinkButtonProps) => (
  <Button
    {...otherProps}
    onClick={() => history.push(to)}
  >
    {children}
  </Button>
)

export const LinkButton = withRouter(LinkButtonComp)
