import React from 'react'
import { CssBaseline } from '@material-ui/core'
import { HashRouter as Router, Switch, Route, Redirect } from 'react-router-dom'
import { CustomAppBar } from './layout/AppBar'
import { Container } from './layout/Container'
import { Login, Register, Classes, Class } from './containers'
import { WithTranslateProps } from './external-types'
import { RtlProvider } from './providers/RtlProvider'
import { createPack } from 'react-component-pack'
import { ServiceProvider } from './providers/ServiceProvider'
import { AuthProvider, useAuth } from './providers/AuthProvider'
import { ClassroomsProvider } from './providers/ClassroomsProvider'

const ProvidersPack = createPack(
  RtlProvider,
  ServiceProvider,
  AuthProvider,
  ClassroomsProvider
)

const Routes = (i18nProps: WithTranslateProps) => {
  const [authState] = useAuth()

  return (
    <Switch>
      <Route path='/login'>
        {authState.token ? <Classes /> : <Login {...i18nProps} />}
      </Route>

      <Route path='/register'>
        <Register {...i18nProps} />
      </Route>

      <Route path='/home'>
        {authState.token ? <Classes /> : <Redirect to='/login' />}
      </Route>

      <Route path='/class'>
        {authState.token ? <Class /> : <Redirect to='/login' />}
      </Route>

      <Route path='/'>
        {authState.token ? <Redirect to='/login' /> : <Redirect to='/home' />}
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
