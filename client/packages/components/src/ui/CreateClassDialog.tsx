import React, { useCallback, useState } from 'react'
import { Button, Dialog, DialogActions, DialogContent, DialogProps, DialogTitle, makeStyles, TextField } from '@material-ui/core'
import { FileButton } from './FileButton'

const useStyles = makeStyles(theme => ({
  nameInput: {
    marginBottom: theme.spacing(2)
  }
}))

interface CreateClassDialogProps extends DialogProps {
  open: boolean
  onFormSubmit(name: string, file: File): void
}

export const CreateClassDialog = ({ open = false, onClose, onFormSubmit }: CreateClassDialogProps) => {
  const classes = useStyles()
  const [studentsFile, setStudentFile] = useState<File>()
  const [className, setClassName] = useState<string>()

  const handleFileChange = useCallback((file: File) => {
    setStudentFile(file)
  }, [setStudentFile])

  const handleNameChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    setClassName(event.target.value)
  }, [setClassName])

  const handleSubmit = useCallback((event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()

    if (className && studentsFile) {
      onFormSubmit(className, studentsFile)
    }
  }, [studentsFile, className])

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth='sm'>
      <DialogTitle>
        Create class
      </DialogTitle>
      <DialogContent>
        <form onSubmit={handleSubmit}>
          <TextField
            label='Class name'
            className={classes.nameInput}
            fullWidth
            onChange={handleNameChange}
          />
          <FileButton
            id='upload-students-file'
            label='Upload students file'
            onFileChange={handleFileChange}
          />
        </form>
      </DialogContent>
      <DialogActions>
        <Button color='primary'>
          Create
        </Button>
      </DialogActions>
    </Dialog>
  )
}
