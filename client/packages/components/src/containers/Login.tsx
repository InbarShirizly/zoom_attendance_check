import React, { useState } from 'react'
import { FormGroup, TextField, Typography, makeStyles, Theme, Button, TextFieldProps } from '@material-ui/core'

const useStyles = makeStyles((theme: Theme) => ({
  label: {
    marginBottom: theme.spacing(3)
  },
  input: {
    marginBottom: theme.spacing(2)
  }
}))

interface InputProps {
  onValueChange(value: string): any
}
const Input = ({ onValueChange, ...props }: TextFieldProps & InputProps) =>
  <TextField
    variant='outlined'
    {...props}
    onChange={e => onValueChange(e.target.value)}
  />

export const Login = () => {
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
      <Typography variant='h4' className={classes.label}>
        Login
      </Typography>
      <form onSubmit={handleSubmit}>
        <FormGroup>
          <Input
            label='Username'
            className={classes.input}
            onValueChange={handleChange('username')}
          />
          <Input
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
