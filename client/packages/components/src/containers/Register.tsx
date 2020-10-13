import React, { useState } from 'react'
import { OutlinedInput } from '../ui/OutlinedInput'
import { FormGroup, Typography, makeStyles, Button } from '@material-ui/core'
import { WithTranslateProps } from '../external-types'
import { Service } from 'services'
import { AuthThunk, useAuth } from '../providers/AuthProvider'
import { useService } from '../providers/ServiceProvider'
import { Alert } from '@material-ui/lab'

const useStyles = makeStyles(theme => ({
  input: {
    marginBottom: theme.spacing(2)
  },
  alert: {
    marginBottom: theme.spacing(2)
  }
}))

interface RegisterState {
  username: string
  password: string
  confirmPasword: string
  email: string
}

const register = (
  service: Service,
  { username, password, confirmPasword, email }: RegisterState
): AuthThunk => async (dispatch, getState) => {
  dispatch({
    type: 'REGISTER',
    username,
    password,
    confirmPasword,
    email
  })

  try {
    const { failed } = getState()
    if (!failed) {
      const { token } = await service.register(username, email, password)
      window.sessionStorage.setItem('token', token)
      return dispatch({
        type: 'AUTH_SUCCESS',
        token
      })
    }
  } catch (e) {
    return dispatch({
      type: 'AUTH_FAILED',
      error: e
    })
  }
}

export const Register = ({ t }: WithTranslateProps) => {
  const classes = useStyles()
  const [service, dispatchService] = useService()
  const [authState, dispatch] = useAuth()
  const [state, setState] = useState<RegisterState>({
    username: '',
    password: '',
    email: '',
    confirmPasword: ''
  })

  const handleChange = (field: string) => (value: string) => setState({ ...state, [field]: value })

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    dispatch(register(service, state))
    dispatchService({
      type: 'SET_TOKEN',
      token: authState.token
    })
  }

  const passwordsMatch = state.password === state.confirmPasword
  const passwordLong = state.password.length >= 4
  const passwordLower = !!state.password.match(/[a-z]/g)
  const passwordUpper = !!state.password.match(/[A-Z]/g)
  const passwordNum = !!state.password.match(/[0-9]/g)

  const passwordValid =
    passwordLong && passwordLower && passwordUpper && passwordNum && passwordsMatch

  return (
    <>
      <Typography variant='h4' gutterBottom>
        {t('register_title')}
      </Typography>
      <form onSubmit={handleSubmit}>
        {authState.failed && (
          <Alert variant='outlined' severity='error' className={classes.alert}>
            Failed to register. Please try again.
          </Alert>
        )}
        <FormGroup>
          <OutlinedInput
            label={t('username')}
            className={classes.input}
            onValueChange={handleChange('username')}
          />
          <OutlinedInput
            label={t('email')}
            className={classes.input}
            type='email'
            onValueChange={handleChange('email')}
          />
          <OutlinedInput
            label={t('password')}
            className={classes.input}
            type='password'
            error={!passwordValid}
            onValueChange={handleChange('password')}
          />
          <OutlinedInput
            label={t('confirm_password')}
            className={classes.input}
            type='password'
            error={!passwordsMatch}
            onValueChange={handleChange('confirmPasword')}
            helperText={!passwordsMatch && t('passwords_dont_match')}
          />
          <Button variant='contained' color='primary' size='large' type='submit'>
            {t('register_title')}
          </Button>
        </FormGroup>
      </form>
    </>
  )
}
