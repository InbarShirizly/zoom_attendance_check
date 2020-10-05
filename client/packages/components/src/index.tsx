import React from 'react'
import { CssBaseline } from '@material-ui/core'
import { HashRouter as Router, Switch, Route, Redirect } from 'react-router-dom'
import { CustomAppBar } from './layout/AppBar'
import { Container } from './layout/Container'
import { Login, Register, Classes } from './containers'
import { WithTranslateProps } from './external-types'

export const Application = (i18nProps: WithTranslateProps) => (
  <>
    <CssBaseline />
    <Router>
      <CustomAppBar {...i18nProps} />

      <Container maxWidth='md'>
        <Switch>
          <Route path='/login'>
            <Login {...i18nProps} />
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
