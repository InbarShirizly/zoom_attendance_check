import React from 'react'
import { Container, CssBaseline } from '@material-ui/core'
import { CustomAppBar } from './layout/AppBar'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
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
