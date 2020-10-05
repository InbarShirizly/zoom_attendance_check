import React, { useState } from 'react'
import {
  AppBar,
  Toolbar,
  Typography,
  makeStyles,
  Button,
  IconButton,
  Menu,
  MenuItem
} from '@material-ui/core'
import { Language } from '@material-ui/icons'
import { WithTranslateProps } from '../external-types'

const useStyles = makeStyles(() => ({
  root: {
    flexGrow: 1
  },
  title: {
    flexGrow: 1
  }
}))

export const CustomAppBar = ({ t, i18n }: WithTranslateProps) => {
  const classes = useStyles()
  const [anchorEl, setAnchorEl] = useState<HTMLElement | null>(null)

  const openMenu = (event: React.MouseEvent<HTMLElement>) => setAnchorEl(event.currentTarget)
  const closeMenu = () => setAnchorEl(null)
  const handleMenuClick = (lang: string) => () => {
    i18n.changeLanguage(lang)
    closeMenu()
  }

  return (
    <AppBar position='fixed'>
      <Toolbar>
        <Typography variant='h6' className={classes.title}>
          {t('app_title')}
        </Typography>

        <Button color='inherit'>Register</Button>
        <Button color='inherit'>Login</Button>

        <IconButton
          color='inherit'
          onClick={openMenu}
        >
          <Language />
        </IconButton>
        <Menu
          anchorEl={anchorEl}
          keepMounted
          open={!!anchorEl}
          onClose={closeMenu}
        >
          <MenuItem onClick={handleMenuClick('en')}>
            {t('en_name')}
          </MenuItem>
          <MenuItem onClick={handleMenuClick('he')}>
            {t('he_name')}
          </MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  )
}
