import React from 'react'
import { TableCell } from '@material-ui/core'
import { Attendance } from 'services'
import { AttendanceIcon } from './AttendanceIcon'

interface AttendanceCellProps {
  attendance: Attendance
}

export const AttendanceCell = ({ attendance }: AttendanceCellProps) => (
  <TableCell
    align='center'
    valign='middle'
  >
    <AttendanceIcon attendance={attendance} />
  </TableCell>
)
