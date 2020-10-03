import React from 'react'
import { CssBaseline, AppBar, Toolbar, Typography, makeStyles, Button } from '@material-ui/core'

const useStyles = makeStyles(() => ({
  root: {
    flexGrow: 1
  },
  title: {
    flexGrow: 1
  }
}))

export const Application = () => {
  const classes = useStyles()

  return (
    <>
      <CssBaseline />
      <AppBar position='fixed'>
        <Toolbar>
          <Typography variant='h6' className={classes.title}>
            Zoom Attendence
          </Typography>

          <Button color='inherit'>Register</Button>
          <Button color='inherit'>Login</Button>
        </Toolbar>
      </AppBar>
    </>
  )
}
