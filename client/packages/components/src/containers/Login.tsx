import React, { useState } from 'react'
import { OutlinedInput } from '../ui/OutlinedInput'
import { WithTranslateProps } from '../external-types'
import { FormGroup, Typography, makeStyles, Theme, Button } from '@material-ui/core'

const useStyles = makeStyles((theme: Theme) => ({
  input: {
    marginBottom: theme.spacing(2)
  }
}))

export const Login = ({ t }: WithTranslateProps) => {
  const classes = useStyles()
  const [state, setState] = useState({
    username: '',
    password: ''
  })

  const handleChange = (field: string) => (value: string) =>
    setState({ ...state, [field]: value })

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    console.log(state)
  }

  return (
    <>
      <Typography variant='h4' gutterBottom>
        {t('login_title')}
      </Typography>
      <form onSubmit={handleSubmit}>
        <FormGroup>
          <OutlinedInput
            label='Username'
            className={classes.input}
            onValueChange={handleChange('username')}
          />
          <OutlinedInput
            label='Password'
            className={classes.input}
            onValueChange={handleChange('password')}
          />
          <Button variant='contained' color='primary' size='large' type='submit'>
            Login
          </Button>
        </FormGroup>
      </form>
    </>
  )
}
