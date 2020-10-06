import React, { useState } from 'react'
import { Table, TableBody, TableCell, TableContainer, TableHead, TablePagination, TableRow } from '@material-ui/core'
import { Attendance, StudentData } from 'services'
import { AttendanceRow } from '../ui/attendance/AttendanceRow'

type RequiredClasses = 'tableContainer'

interface AttendanceTableProps {
  students: StudentData[]
  classes: Record<RequiredClasses | string, string>
}

export const AttendanceTable = ({ students, classes }: AttendanceTableProps) => {
  const [page, setPage] = useState(0)
  const [rowsPerPage, setRowsPerPage] = useState(10)

  const handleChangePage = (event: unknown, newPage: number) => setPage(newPage)

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10))
    setPage(0)
  }

  const studentsInPage = students.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)

  return (
    <>
      <TableContainer className={classes.tableContainer}>
        <Table stickyHeader>
          <TableHead>
            <TableRow>
              <TableCell>
                Name
              </TableCell>
              <TableCell align='center' valign='middle'>
                3.10
              </TableCell>
              <TableCell align='center' valign='middle'>
                4.10
              </TableCell>
              <TableCell align='center' valign='middle'>
                5.10
              </TableCell>
              <TableCell align='center' valign='middle'>
                3.10
              </TableCell>
              <TableCell align='center' valign='middle'>
                4.10
              </TableCell>
              <TableCell align='center' valign='middle'>
                5.10
              </TableCell>
              <TableCell align='center' valign='middle'>
                3.10
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {studentsInPage.map(s => (
              <AttendanceRow
                key={s.id}
                student={s}
                attendances={[
                  Attendance.Attended,
                  Attendance.Partial,
                  Attendance.Absent,
                  Attendance.Attended,
                  Attendance.Partial,
                  Attendance.Absent,
                  Attendance.Attended
                ]}
              />
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        rowsPerPageOptions={[10, 15, 30]}
        component='div'
        count={students.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onChangePage={handleChangePage}
        onChangeRowsPerPage={handleChangeRowsPerPage}
      />
    </>
  )
}
