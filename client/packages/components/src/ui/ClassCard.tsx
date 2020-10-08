import React from 'react'
import {
  Card,
  CardActions,
  CardContent,
  Divider,
  Grid,
  Typography
} from '@material-ui/core'
import { LinkButton } from './LinkButton'
import { ShallowClassroom } from 'services'

interface ClassCardProps {
  classroom: ShallowClassroom
}

export const ClassCard = ({ classroom }: ClassCardProps) => (
  <Grid item md={4} sm={6} xs={12}>
    <Card elevation={2}>
      <CardContent>
        <Typography variant='h5'>
          {classroom.name}
        </Typography>
      </CardContent>
      <Divider />
      <CardActions>
        <LinkButton
          to={`/class/${classroom.id}`}
          size='small'
          color='primary'
        >
          Create Report
        </LinkButton>
      </CardActions>
    </Card>
  </Grid>
)
