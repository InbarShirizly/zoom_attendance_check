import React, { useEffect, useState } from 'react'
import { Divider, Fab, makeStyles, Paper, Tab, Tabs, Typography } from '@material-ui/core'
import { Add as AddIcon } from '@material-ui/icons'
import { StudentDataTable } from '../layout/StudentsDataTable'
import { AttendanceTable } from '../layout/AttendanceTable'
import { StudentData } from 'services'
import { useClassrooms } from '../providers/ClassroomsProvider'
import { withRouter, RouteComponentProps } from 'react-router-dom'
import { useService } from '../providers/ServiceProvider'
import { createClassroomActions } from '../actions/classroom'
import { CreateReportDialog } from '../ui/CreateReportDialog'

enum TabType {
  StudentData = 0,
  Attendance = 1
}

const useStyles = makeStyles(theme => ({
  fab: {
    position: 'fixed',
    bottom: theme.spacing(2),
    right: theme.spacing(2)
  },
  tableContainer: {
    maxHeight: 587
  }
}))

interface TableByTabProps {
  tabType: TabType
  students: StudentData[]
}

const TableByTabType = ({ tabType, students }: TableByTabProps) => {
  const classes = useStyles()

  switch (tabType) {
    case TabType.StudentData:
      return <StudentDataTable students={students} classes={classes} />
    case TabType.Attendance:
      return <AttendanceTable students={students} classes={classes} />
  }
}

const ClassComp = ({ match, history }: RouteComponentProps<{ id: string }>) => {
  const classes = useStyles()
  const [service] = useService()
  const [{ selectedClassroom }, dispatch] = useClassrooms()
  const [tabValue, setTabValue] = useState(TabType.StudentData)
  const [open, setOpen] = useState(false)

  const handleOpen = () => setOpen(true)
  const handleClose = () => setOpen(false)

  const handleChange = (event: React.ChangeEvent<{}>, newValue: TabType) => setTabValue(newValue)

  const actions = createClassroomActions(service)

  useEffect(() => {
    const id = parseInt(match.params.id, 10)
    if (!isNaN(id)) {
      dispatch(actions.select(id))
    } else {
      history.push('/')
    }
  }, [])

  if (!selectedClassroom) {
    history.push('/')
    return <></> // To comply with TS compiler
  }

  return (
    <>
      <CreateReportDialog
        open={open}
        onClose={handleClose}
        onFormSubmit={() => {}}
      />
      <Typography variant='h4' gutterBottom>
        {selectedClassroom.name}
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

        <Divider />

        <TableByTabType
          tabType={tabValue}
          students={selectedClassroom.students}
        />
      </Paper>

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

export const Class = withRouter(ClassComp)
