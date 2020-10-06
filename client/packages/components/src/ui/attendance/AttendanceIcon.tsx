import React from 'react'
import { Attendance } from 'services'
import { makeStyles, createStyles, Theme } from '@material-ui/core'
import { Cancel, CheckCircle, Warning } from '@material-ui/icons'

interface AttendanceIconProps {
  attendance: Attendance
}

const colorForAttendance = (attendance: Attendance, theme: Theme) => {
  switch (attendance) {
    case Attendance.Absent:
      return theme.palette.error.dark
    case Attendance.Attended:
      return theme.palette.success.main
    case Attendance.Partial:
      return theme.palette.warning.main
  }
}

const useStyles = (attendance: Attendance) => makeStyles(theme => createStyles({
  root: {
    marginTop: 7,
    fill: colorForAttendance(attendance, theme)
  }
}))()

export const AttendanceIcon = ({ attendance }: AttendanceIconProps) => {
  const classes = useStyles(attendance)

  switch (attendance) {
    case Attendance.Absent:
      return <Cancel color='error' classes={classes} />
    case Attendance.Attended:
      return <CheckCircle classes={classes} />
    case Attendance.Partial:
      return <Warning classes={classes} />
  }
}
