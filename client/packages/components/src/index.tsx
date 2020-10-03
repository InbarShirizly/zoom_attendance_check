import React from 'react'
import { CssBaseline } from '@material-ui/core'
import { HashRouter as Router, Switch, Route, Redirect } from 'react-router-dom'
import { CustomAppBar } from './layout/AppBar'
import { Container } from './layout/Container'
import { Login } from './containers/Login'

export const Application = () => (
  <>
    <CssBaseline />
    <Router>
      <CustomAppBar />

      <Container maxWidth='md'>
        <Switch>
          <Route path='/login'>
            <Login />
          </Route>

          <Route path='/'>
            <Redirect to='/login' />
          </Route>
        </Switch>
      </Container>
    </Router>
  </>
)
