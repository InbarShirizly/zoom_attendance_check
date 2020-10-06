import React from 'react'
import { makeStyles, TableCell } from '@material-ui/core'
import { Attendance } from 'services'
import { AttendanceIcon } from './AttendanceIcon'

interface AttendanceCellProps {
  attendance: Attendance
}

const useStyles = makeStyles({
  root: {
    paddingTop: 0,
    paddingRight: 0,
    paddingBottom: 0,
    paddingLeft: 4
  }
})

export const AttendanceCell = ({ attendance }: AttendanceCellProps) => {
  const classes = useStyles()

  return (
    <TableCell
      align='center'
      valign='middle'
      classes={classes}
    >
      <AttendanceIcon attendance={attendance} />
    </TableCell>
  )
}
