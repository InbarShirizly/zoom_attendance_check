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
import { useTextDirection } from '../providers'

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
  const [_, setTextDirection] = useTextDirection()

  const openMenu = (event: React.MouseEvent<HTMLElement>) => setAnchorEl(event.currentTarget)
  const closeMenu = () => setAnchorEl(null)
  const handleMenuClick = (lang: string) => () => {
    i18n.changeLanguage(lang)
    setTextDirection({
      type: lang === 'he' ? 'SET_RTL' : 'SET_LTR'
    })
    closeMenu()
  }

  return (
    <AppBar position='fixed' data-testid='appbar'>
      <Toolbar>
        <Typography variant='h6' className={classes.title} data-testid='app-title'>
          {t('app_title')}
        </Typography>

        <Button color='inherit'>
          {t('register_title')}
        </Button>
        <Button color='inherit'>
          {t('login_title')}
        </Button>

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
          data-testid='language-menu'
        >
          <MenuItem onClick={handleMenuClick('en')} data-testid='english-button'>
            {t('en_name')}
          </MenuItem>
          <MenuItem onClick={handleMenuClick('he')} data-testid='hebrew-button'>
            {t('he_name')}
          </MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  )
}
