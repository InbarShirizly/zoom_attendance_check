import React, { useState } from 'react'
import { OutlinedInput } from '../ui/OutlinedInput'
import { FormGroup, Typography, makeStyles, Theme, Button } from '@material-ui/core'
import { WithTranslateProps } from '../external-types'

const useStyles = makeStyles((theme: Theme) => ({
  input: {
    marginBottom: theme.spacing(2)
  }
}))

export const Register = ({ t }: WithTranslateProps) => {
  const classes = useStyles()
  const [state, setState] = useState({
    username: '',
    password: '',
    email: '',
    confirmPasword: ''
  })

  const handleChange = (field: string) => (value: string) =>
    setState({ ...state, [field]: value })

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    console.log(state)
  }

  const passwordsMatch = state.password === state.confirmPasword

  return (
    <>
      <Typography variant='h4' gutterBottom>
        {t('register_title')}
      </Typography>
      <form onSubmit={handleSubmit}>
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
            error={!passwordsMatch}
            onValueChange={handleChange('password')}
          />
          <OutlinedInput
            label={t('confirm_password')}
            className={classes.input}
            type='password'
            error={!passwordsMatch}
            onValueChange={handleChange('confirmPasword')}
            helperText={!passwordsMatch && 'Passwords don\'t match'}
          />
          <Button variant='contained' color='primary' size='large' type='submit'>
            {t('register_title')}
          </Button>
        </FormGroup>
      </form>
    </>
  )
}
