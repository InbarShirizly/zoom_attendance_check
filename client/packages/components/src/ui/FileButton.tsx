import React from 'react'
import { Button, makeStyles } from '@material-ui/core'

const useStyles = makeStyles({
  input: {
    display: 'none'
  }
})

interface FileButtonProps {
  id: string
  label: string
  onFileChange(file: File): void
}

// TODO - Add accept field
export const FileButton = ({ id, onFileChange, label }: FileButtonProps) => {
  const classes = useStyles()

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const [file] = Array.from(event.currentTarget.files ?? [])

    if (file) {
      onFileChange(file)
    }
  }

  return (
    <>
      <input
        className={classes.input}
        id={id}
        onChange={handleChange}
        type='file'
      />
      <label htmlFor={id}>
        <Button variant='contained' color='primary' component='span'>
          {label}
        </Button>
      </label>
    </>
  )
}
