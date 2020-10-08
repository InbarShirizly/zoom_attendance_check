import React, { useCallback, useState } from 'react'
import { Button, Dialog, DialogActions, DialogContent, DialogProps, DialogTitle, makeStyles, TextField } from '@material-ui/core'
import { FileButton } from './FileButton'

const useStyles = makeStyles(theme => ({
  nameInput: {
    marginTop: theme.spacing(1),
    marginBottom: theme.spacing(1)
  }
}))

interface CreateReportDialogProps extends DialogProps {
  open: boolean
  onFormSubmit(name: string, file: File): void
}

export const CreateReportDialog = ({ open = false, onClose, onFormSubmit }: CreateReportDialogProps) => {
  const classes = useStyles()
  const [studentsFile, setStudentFile] = useState<File>()
  const [description, setDescription] = useState<string>()

  const handleFileChange = useCallback((file: File) => {
    setStudentFile(file)
  }, [setStudentFile])

  const handleDescription = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    setDescription(event.target.value)
  }, [description])

  const handleSubmit = useCallback(() => {
    if (description && studentsFile) {
      onFormSubmit(description, studentsFile)
    }
  }, [description, studentsFile])

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth='sm'>
      <DialogTitle>
        Create report
      </DialogTitle>
      <DialogContent>
        <form
          onSubmit={event => {
            event.preventDefault()
            handleSubmit()
          }}
        >
          <TextField
            label='Report description'
            className={classes.nameInput}
            fullWidth
            onChange={handleDescription}
            helperText='Short description about the report.'
          />
          <FileButton
            id='upload-students-file'
            label='Select chat file'
            onFileChange={handleFileChange}
          />
          <TextField
            label='Time Delta'
            className={classes.nameInput}
            fullWidth
            onChange={handleDescription}
            type='number'
            helperText='The time for parsing each session, in minutes.'
          />
          <TextField
            label='First sentence'
            className={classes.nameInput}
            fullWidth
            onChange={handleDescription}
            type='number'
            helperText='Sentence for starting a session.'
          />
          <TextField
            label='Excluded Zoom users'
            className={classes.nameInput}
            fullWidth
            onChange={handleDescription}
            type='number'
            helperText='Zoom users to exclude from parsing, separated by a comma.'
          />
        </form>
      </DialogContent>
      <DialogActions>
        <Button
          color='primary'
          onClick={handleSubmit}
        >
          Create
        </Button>
      </DialogActions>
    </Dialog>
  )
}
