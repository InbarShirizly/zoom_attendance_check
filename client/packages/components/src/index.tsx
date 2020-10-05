import React from 'react'
import { createMuiTheme, CssBaseline, ThemeProvider } from '@material-ui/core'
import { HashRouter as Router, Switch, Route, Redirect } from 'react-router-dom'
import { CustomAppBar } from './layout/AppBar'
import { Container } from './layout/Container'
import { Login, Register, Classes } from './containers'
import { WithTranslateProps } from './external-types'

const theme = createMuiTheme({
  typography: {
    fontFamily: '"Heebo", "HelveticaNeue-Light", "Helvetica Neue Light", "Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif'
  }
})

export const Application = (i18nProps: WithTranslateProps) => (
  <ThemeProvider theme={theme}>
    <CssBaseline />
    <Router>
      <CustomAppBar {...i18nProps} />

      <Container maxWidth='md'>
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

          <Route path='/'>
            <Redirect to='/login' />
          </Route>
        </Switch>
      </Container>
    </Router>
  </ThemeProvider>
)
