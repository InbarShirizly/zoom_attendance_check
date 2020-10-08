import React, { useEffect, useState } from 'react'
import { Add as AddIcon } from '@material-ui/icons'
import { Fab, Grid, makeStyles, Theme, Typography } from '@material-ui/core'
import { ClassCard } from '../ui/ClassCard'
import { CreateClassDialog } from '../ui/CreateClassDialog'
import { useService } from '../providers/ServiceProvider'
import { useAuth } from '../providers/AuthProvider'
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
  const [authState] = useAuth()
  const [service] = useService()
  const [{ classrooms }, dispatch] = useClassrooms()
  const [open, setOpen] = useState(false)

  const handleOpen = () => setOpen(true)
  const handlClose = () => setOpen(false)

  const actions = createClassroomActions(service, authState.token)

  useEffect(() => {
    dispatch(actions.fetch())
  }, [])

  return (
    <>
      <CreateClassDialog
        open={open}
        onClose={handlClose}
        onFileChange={() => {}}
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
