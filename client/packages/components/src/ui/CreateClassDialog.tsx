import React from 'react'
import { Button, Dialog, DialogActions, DialogContent, DialogProps, DialogTitle, makeStyles, TextField } from '@material-ui/core'
import { FileButton } from './FileButton'

const useStyles = makeStyles(theme => ({
  nameInput: {
    marginBottom: theme.spacing(2)
  }
}))

interface CreateClassDialogProps extends DialogProps {
  open: boolean
  onFileChange(file: File): void
}

export const CreateClassDialog = ({ open = false, onClose, onFileChange }: CreateClassDialogProps) => {
  const classes = useStyles()

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth='sm'>
      <DialogTitle>
        Create class
      </DialogTitle>
      <DialogContent>
        <form>
          <TextField
            label='Class name'
            className={classes.nameInput}
            fullWidth
          />
          <FileButton
            id='upload-students-file'
            label='Upload students file'
            onFileChange={onFileChange}
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
