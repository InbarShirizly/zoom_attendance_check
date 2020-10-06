import React from 'react'
import { Divider, Table, TableBody, TableCell, TableHead, TableRow } from '@material-ui/core'

export const StudentDataTable = () => {
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
              Phone
            </TableCell>
            <TableCell>
              ID Number
            </TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          <TableRow>
            <TableCell>
              Jonathan Ohayon
            </TableCell>
            <TableCell>
              0501234567
            </TableCell>
            <TableCell>
              123456789
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </>
  )
}
