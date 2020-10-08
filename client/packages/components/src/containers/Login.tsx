import React, { Dispatch, useState } from 'react'
import { OutlinedInput } from '../ui/OutlinedInput'
import { WithTranslateProps } from '../external-types'
import { FormGroup, Typography, makeStyles, Button } from '@material-ui/core'
import { Alert } from '@material-ui/lab'
import { Service } from 'services'
import { AuthThunk, useAuth } from '../providers/AuthProvider'
import { useService } from '../providers/ServiceProvider'

const useStyles = makeStyles(theme => ({
  input: {
    marginBottom: theme.spacing(2)
  },
  alert: {
    marginBottom: theme.spacing(2)
  }
}))

interface LoginState {
  username: string
  password: string
}

const login = (service: Service, { username, password }: LoginState): AuthThunk => async dispatch => {
  dispatch({
    type: 'LOGIN',
    username,
    password
  })

  try {
    const { token } = await service.login(username, password)
    window.sessionStorage.setItem('token', token)
    return dispatch({
      type: 'AUTH_SUCCESS',
      token
    })
  } catch (e) {
    return dispatch({
      type: 'AUTH_FAILED',
      error: e
    })
  }
}

export const Login = ({ t }: WithTranslateProps) => {
  const classes = useStyles()
  const [service, dispatchService] = useService()
  const [authState, dispatch] = useAuth()
  const [state, setState] = useState<LoginState>({
    username: '',
    password: ''
  })

  const handleChange = (field: string) => (value: string) =>
    setState({ ...state, [field]: value })

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    dispatch(login(service, state))
    dispatchService({
      type: 'SET_TOKEN',
      token: authState.token
    })
  }

  return (
    <>
      <Typography variant='h4' gutterBottom>
        {t('login_title')}
      </Typography>
      <form onSubmit={handleSubmit}>
        {
          authState.failed &&
          <Alert
            variant='outlined'
            severity='error'
            className={classes.alert}
          >
            Failed to login. Please try again.
          </Alert>
        }
        <FormGroup>
          <OutlinedInput
            label={t('username')}
            className={classes.input}
            onValueChange={handleChange('username')}
          />
          <OutlinedInput
            label={t('password')}
            type='password'
            className={classes.input}
            onValueChange={handleChange('password')}
          />
          <Button variant='contained' color='primary' size='large' type='submit'>
            {t('login_title')}
          </Button>
        </FormGroup>
      </form>
    </>
  )
}
