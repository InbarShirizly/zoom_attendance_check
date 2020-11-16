import React, { useCallback, useState } from 'react'
import { Button, Grid, makeStyles, Typography } from '@material-ui/core'

const useStyles = makeStyles(theme => ({
  input: {
    display: 'none'
  },
  label: {
    marginLeft: theme.spacing(1)
  }
}))

interface FileButtonProps {
  id: string
  label: string
  onFileChange(file: File): void
}

// TODO - Add accept field
export const FileButton = ({ id, onFileChange, label }: FileButtonProps) => {
  const classes = useStyles()
  const [filename, setFilename] = useState<string>()

  const handleChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const [file] = Array.from(event.currentTarget.files ?? [])

    if (file) {
      onFileChange(file)
      setFilename(file.name)
    }
  }, [setFilename])

  return (
    <>
      <input
        className={classes.input}
        id={id}
        onChange={handleChange}
        type='file'
      />
      <Grid
        container
        alignItems='center'
        component='span'
        direction='row'
      >
        <Button variant='contained' color='primary'>
          <label htmlFor={id}>
            {label}
          </label>
        </Button>
        <Typography className={classes.label}>
          {filename || 'No file selected'}
        </Typography>
      </Grid>
    </>
  )
}
