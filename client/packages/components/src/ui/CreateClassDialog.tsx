import React from 'react'
import { Button, Dialog, DialogActions, DialogContent, DialogProps, DialogTitle, TextField } from '@material-ui/core'

interface CreateClassDialogProps extends DialogProps {
  open: boolean
}

export const CreateClassDialog = ({ open = false, onClose }: CreateClassDialogProps) => {
  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth='sm'>
      <DialogTitle>
        Create class
      </DialogTitle>
      <DialogContent>
        <form>
          <TextField
            label='Class name'
            fullWidth
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
