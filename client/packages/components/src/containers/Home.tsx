import React, { useEffect, useState } from 'react'
import { Add as AddIcon } from '@material-ui/icons'
import { Fab, Grid, makeStyles, Theme, Typography } from '@material-ui/core'
import { Alert } from '@material-ui/lab'
import { useLocation } from 'react-router-dom'
import { ClassCard } from '../ui/ClassCard'
import { CreateClassDialog } from '../ui/CreateClassDialog'
import { useService } from '../providers/ServiceProvider'
import { createClassroomActions } from '../actions/classroom'
import { useClassrooms } from '../providers/ClassroomsProvider'

const useStyles = makeStyles((theme: Theme) => ({
  fab: {
    position: 'fixed',
    bottom: theme.spacing(2),
    right: theme.spacing(2)
  },
  alert: {
    marginBottom: theme.spacing(2)
  }
}))

export const Classes = () => {
  const classes = useStyles()
  // Adding any cast here because for some reason this is coming back as Location<unknown>
  const location = useLocation() as any
  const [service] = useService()
  const [{ classrooms }, dispatch] = useClassrooms()
  const [open, setOpen] = useState(false)

  const handleOpen = () => setOpen(true)
  const handleClose = () => setOpen(false)

  const actions = createClassroomActions(service)

  useEffect(() => {
    dispatch(actions.fetchAll())
  }, [])

  return (
    <>
      <CreateClassDialog
        open={open}
        onClose={handleClose}
        onFormSubmit={(name, file) => {
          dispatch(actions.create(name, file))
          handleClose()
        }}
      />

      {location.state?.registrationSuccess && (
        <Alert variant='outlined' severity={'success'} className={classes.alert}>
          Registration successful!
        </Alert>
      )}

      <Typography variant='h4' gutterBottom>
        My Classes
      </Typography>

      <Grid container spacing={3}>
        {classrooms.map(c => <ClassCard classroom={c} key={c.id} />)}
      </Grid>

      <Fab
        className={classes.fab}
        color='primary'
        onClick={handleOpen}
      >
        <AddIcon />
      </Fab>
    </>
  )
}
