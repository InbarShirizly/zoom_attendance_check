import React, { useState } from 'react'
import { Fab, makeStyles, Paper, Tab, Tabs, Typography } from '@material-ui/core'
import { StudentDataTable } from '../layout/StudentsDataTable'
import { Add as AddIcon } from '@material-ui/icons'

const useStyles = makeStyles(theme => ({
  fab: {
    position: 'fixed',
    bottom: theme.spacing(2),
    right: theme.spacing(2)
  }
}))

const testStudents = (new Array(30)).fill('').map((_, i) => ({
  id: i,
  classId: 1,
  name: 'John Doe',
  phone: 501234560 + i,
  idNumber: '123456789'
}))

export const Class = () => {
  const classes = useStyles()
  const [value, setValue] = useState(0)

  const handleChange = (event: React.ChangeEvent<{}>, newValue: number) => setValue(newValue)

  return (
    <>
      <Typography variant='h4' gutterBottom>
        Physics
      </Typography>

      <Paper elevation={2}>
        <Tabs
          value={value}
          onChange={handleChange}
          indicatorColor='primary'
          textColor='primary'
          centered
        >
          <Tab label='Student Data' />
          <Tab label='Attendence' />
        </Tabs>

        <StudentDataTable students={testStudents} />
      </Paper>

      <Fab
        className={classes.fab}
        color='primary'
      >
        <AddIcon />
      </Fab>
    </>
  )
}
