import React, { useState } from 'react'
import { Fab, makeStyles, Paper, Tab, Tabs, Typography } from '@material-ui/core'
import { StudentDataTable } from '../layout/StudentsDataTable'
import { Add as AddIcon } from '@material-ui/icons'
import { AttendanceTable } from '../layout/AttendanceTable'
import { StudentData } from 'services'

enum TabType {
  StudentData = 0,
  Attendance = 1
}

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

interface TableByTabProps {
  tabType: TabType
  students: StudentData[]
}

const TableByTabType = ({ tabType, students }: TableByTabProps) => {
  switch (tabType) {
    case TabType.StudentData:
      return <StudentDataTable students={students} />
    case TabType.Attendance:
      return <AttendanceTable students={students} />
  }
}

export const Class = () => {
  const classes = useStyles()
  const [tabValue, setTabValue] = useState(TabType.StudentData)

  const handleChange = (event: React.ChangeEvent<{}>, newValue: TabType) => setTabValue(newValue)

  return (
    <>
      <Typography variant='h4' gutterBottom>
        Physics
      </Typography>

      <Paper elevation={2}>
        <Tabs
          value={tabValue}
          onChange={handleChange}
          indicatorColor='primary'
          textColor='primary'
          centered
        >
          <Tab label='Student Data' />
          <Tab label='Attendance' />
        </Tabs>

        <TableByTabType
          tabType={tabValue}
          students={testStudents}
        />
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
