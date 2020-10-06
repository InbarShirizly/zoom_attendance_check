import React from 'react'
import { Container as MdContainer, ContainerProps, Theme, useTheme, withStyles } from '@material-ui/core'

const createContainer = (theme: Theme) => withStyles({
  root: {
    marginTop: 100,
    marginBottom: theme.spacing(2)
  }
})(MdContainer)

export const Container = (props: ContainerProps) => {
  const theme = useTheme()
  const BlankContainer = createContainer(theme)

  return <BlankContainer {...props} />
}
