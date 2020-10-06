import React, { useState } from 'react'
import { Divider, Table, TableBody, TableCell, TableHead, TablePagination, TableRow } from '@material-ui/core'
import { StudentData } from 'services'

interface StudentDataTableProps {
  students: StudentData[]
}

export const AttendenceTable = ({ students }: StudentDataTableProps) => {
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
      <Divider />
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>
              Name
            </TableCell>
            <TableCell>
              3.10
            </TableCell>
            <TableCell>
              4.10
            </TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {studentsInPage.map(s => (
            <TableRow key={s.id}>
              <TableCell>
                {s.name}
              </TableCell>
              <TableCell>
                {s.phone}
              </TableCell>
              <TableCell>
                {s.idNumber}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
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
