import { Container as MdContainer, createStyles, withStyles } from '@material-ui/core'

export const Container = withStyles(theme => createStyles({
  root: {
    marginTop: 100,
    marginBottom: theme.spacing(2)
  }
}))(MdContainer)
