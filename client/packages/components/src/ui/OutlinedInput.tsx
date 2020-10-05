import React from 'react'
import { TextField, TextFieldProps } from '@material-ui/core'

interface InputProps {
  onValueChange(value: string): any
}

export const OutlinedInput = ({ onValueChange, ...props }: TextFieldProps & InputProps) =>
  <TextField
    variant='outlined'
    {...props}
    onChange={e => onValueChange(e.target.value)}
  />
