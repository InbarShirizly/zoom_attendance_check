import React from 'react'
import { CssBaseline } from '@material-ui/core'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import { CustomAppBar } from './layout/AppBar'
import { Container } from './layout/Container'
import { Login } from './containers/Login'

export const Application = () => (
  <>
    <CssBaseline />
    <Router>
      <CustomAppBar />

      <Container maxWidth='lg'>
        <Switch>
          <Route path='/'>
            <Login />
          </Route>
        </Switch>
      </Container>
    </Router>
  </>
)
