import React, { useEffect, useState } from 'react'
import { Add as AddIcon } from '@material-ui/icons'
import { Fab, Grid, makeStyles, Theme, Typography } from '@material-ui/core'
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
  }
}))

export const Classes = () => {
  const classes = useStyles()
  const [service] = useService()
  const [{ classrooms }, dispatch] = useClassrooms()
  const [open, setOpen] = useState(false)

  const handleOpen = () => setOpen(true)
  const handleClose = () => setOpen(false)

  const actions = createClassroomActions(service)

  useEffect(() => {
    dispatch(actions.fetch())
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

      <Typography variant='h4' gutterBottom>
        My Classes
      </Typography>

      <Grid container spacing={3}>
        {classrooms.map(({ name, id }) => <ClassCard name={name} key={id} />)}
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
