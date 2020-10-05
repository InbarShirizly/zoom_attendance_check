import React, { useState } from 'react'
import { Add as AddIcon } from '@material-ui/icons'
import { Fab, Grid, makeStyles, Theme, Typography } from '@material-ui/core'
import { ClassCard } from '../ui/ClassCard'
import { CreateClassDialog } from '../ui/CreateClassDialog'

const useStyles = makeStyles((theme: Theme) => ({
  fab: {
    position: 'fixed',
    bottom: theme.spacing(2),
    right: theme.spacing(2)
  }
}))

const data = (new Array(10)).fill('Class Name')

export const Classes = () => {
  const classes = useStyles()
  const [open, setOpen] = useState(false)

  const handleOpen = () => setOpen(true)
  const handlClose = () => setOpen(false)

  return (
    <>
      <CreateClassDialog
        open={open}
        onClose={handlClose}
      />

      <Typography variant='h4' gutterBottom>
        My Classes
      </Typography>

      <Grid container spacing={3}>
        {data.map((d, i) => <ClassCard name={d} key={i} />)}
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
