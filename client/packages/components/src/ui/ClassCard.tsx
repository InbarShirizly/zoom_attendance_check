import React from 'react'
import {
  Button,
  Card,
  CardActions,
  CardContent,
  Divider,
  Grid,
  Typography
} from '@material-ui/core'

interface ClassCardProps {
  name: string;
}

export const ClassCard = ({ name }: ClassCardProps) => (
  <Grid item md={4} sm={6} xs={12}>
    <Card elevation={2}>
      <CardContent>
        <Typography variant='h5'>
          {name}
        </Typography>
      </CardContent>
      <Divider />
      <CardActions>
        <Button size='small' color='primary'>
          Create Report
        </Button>
      </CardActions>
    </Card>
  </Grid>
)
