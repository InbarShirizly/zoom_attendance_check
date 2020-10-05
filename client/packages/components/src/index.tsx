import React from 'react'
import { CssBaseline } from '@material-ui/core'
import { HashRouter as Router, Switch, Route, Redirect } from 'react-router-dom'
import { CustomAppBar } from './layout/AppBar'
import { Container } from './layout/Container'
import { Login, Register, Classes } from './containers'

interface ApplicationProps {
  t(key: string): string | undefined | null
}

export const Application = ({ t }: ApplicationProps) => (
  <>
    <CssBaseline />
    <Router>
      <CustomAppBar />

      <Container maxWidth='md'>
        <Switch>
          <Route path='/login'>
            <Login t={t} />
          </Route>

          <Route path='/register'>
            <Register />
          </Route>

          <Route path='/home'>
            <Classes />
          </Route>

          <Route path='/'>
            <Redirect to='/login' />
          </Route>
        </Switch>
      </Container>
    </Router>
  </>
)
