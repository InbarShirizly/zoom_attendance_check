import React from 'react'
import { TableCell, TableRow } from '@material-ui/core'
import { Attendance, StudentData } from 'services'
import { AttendanceCell } from './AttendanceCell'

interface AttendanceRowProps {
  student: StudentData
  attendances: Attendance[]
}

export const AttendanceRow = ({ student, attendances }: AttendanceRowProps) => (
  <TableRow>
    <TableCell>
      {student.name}
    </TableCell>
    {attendances.map((a, i) =>
      <AttendanceCell key={i} attendance={a} />
    )}
  </TableRow>
)
