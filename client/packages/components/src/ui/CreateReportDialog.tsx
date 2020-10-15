import React, { useCallback, useState } from 'react'
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogProps,
  DialogTitle,
  makeStyles,
  TextField
} from '@material-ui/core'
import { FileButton } from './FileButton'

const useStyles = makeStyles(theme => ({
  nameInput: {
    marginTop: theme.spacing(1),
    marginBottom: theme.spacing(1)
  }
}))

interface CreateReportDialogProps extends DialogProps {
  open: boolean
  classId: number

  /**
   * Makes a request to create a new report in the server.
   */
  onFormSubmit(
    id: number,
    file: File,
    timeDelta: number,
    firstSentence: string,
    excludedUsers: string,
    description: string
  ): number
}

/**
 * Form dialog for creating a new report for the selected class.
 */
export const CreateReportDialog = ({
  open = false,
  onClose,
  classId,
  onFormSubmit
}: CreateReportDialogProps) => {
  const classes = useStyles()
  const [studentsFile, setStudentFile] = useState<File>()
  const [description, setDescription] = useState<string>()
  const [excludedUsers, setExcludedUsers] = useState<string>()
  const [firstSentence, setFirstSentence] = useState<string>()
  const [timeDelta, setTimeDelta] = useState<number>()

  const handleFileChange = useCallback(
    (file: File) => {
      setStudentFile(file)
    },
    [setStudentFile]
  )

  const handleDescription = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      setDescription(event.target.value)
    },
    [description]
  )

  const handleTimeDelta = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      setTimeDelta(parseInt(event.target.value))
    },
    [timeDelta]
  )

  const handleExcludedUsers = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      setExcludedUsers(event.target.value)
    },
    [excludedUsers]
  )

  const handleFirstSentence = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      setFirstSentence(event.target.value)
    },
    [firstSentence]
  )

  const handleSubmit = useCallback(() => {
    if (description && studentsFile && timeDelta && firstSentence && excludedUsers) {
      onFormSubmit(classId, studentsFile, timeDelta, firstSentence, excludedUsers, description)
    }
  }, [description, studentsFile, excludedUsers, firstSentence, timeDelta])

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth='sm'>
      <DialogTitle>Create report</DialogTitle>
      <DialogContent>
        <form
          onSubmit={event => {
            event.preventDefault()
            handleSubmit()
          }}>
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
            onChange={handleTimeDelta}
            type='number'
            helperText='The time for parsing each session, in minutes.'
          />
          <TextField
            label='First sentence'
            className={classes.nameInput}
            fullWidth
            onChange={handleFirstSentence}
            type='text'
            helperText='Sentence for starting a session.'
          />
          {/* maybe implement this like gmail */}
          <TextField
            label='Excluded Zoom users'
            className={classes.nameInput}
            fullWidth
            onChange={handleExcludedUsers}
            type='text'
            helperText='Zoom users to exclude from parsing, separated by a comma.'
          />
        </form>
      </DialogContent>
      <DialogActions>
        <Button color='primary' onClick={handleSubmit}>
          Create
        </Button>
      </DialogActions>
    </Dialog>
  )
}
