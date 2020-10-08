import React from 'react'
import { CssBaseline } from '@material-ui/core'
import { HashRouter as Router, Switch, Route, Redirect } from 'react-router-dom'
import { CustomAppBar } from './layout/AppBar'
import { Container } from './layout/Container'
import { Login, Register, Classes, Class } from './containers'
import { WithTranslateProps } from './external-types'
import { RtlProvider } from './providers'
import { createPack } from 'react-component-pack'
import { ServiceProvider } from './providers/ServiceProvider'
import { AuthProvider } from './providers/AuthProvider'

const ProvidersPack = createPack(
  RtlProvider,
  ServiceProvider,
  AuthProvider
)

const Routes = (i18nProps: WithTranslateProps) => {
  return (
    <Switch>
      <Route path='/login'>
        <Login {...i18nProps} />
      </Route>

      <Route path='/register'>
        <Register {...i18nProps} />
      </Route>

      <Route path='/home'>
        <Classes />
      </Route>

      <Route path='/class'>
        <Class />
      </Route>

      <Route path='/'>
        <Redirect to='/login' />
      </Route>
    </Switch>
  )
}

export const Application = (i18nProps: WithTranslateProps) => (
  <ProvidersPack>
    <CssBaseline />
    <Router>
      <CustomAppBar {...i18nProps} />

      <Container maxWidth='md'>
        <Routes {...i18nProps}/>
      </Container>
    </Router>
  </ProvidersPack>
)
