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
import { useTextDirection } from '../providers/RtlProvider'
import { LinkButton } from '../ui/LinkButton'
import { AuthThunk, useAuth } from '../providers/AuthProvider'
import { RouteComponentProps, withRouter } from 'react-router-dom'

const useStyles = makeStyles(() => ({
  root: {
    flexGrow: 1
  },
  title: {
    flexGrow: 1
  }
}))

const CustomAppBarComponent = ({ t, i18n, history }: WithTranslateProps & RouteComponentProps) => {
  const classes = useStyles()
  const [authState, dispatch] = useAuth()
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

  const logout = (): AuthThunk => dispatch => {
    window.sessionStorage.removeItem('token')
    dispatch({ type: 'LOGOUT' })
    return history.push('/')
  }

  return (
    <AppBar position='fixed' data-testid='appbar'>
      <Toolbar>
        <Typography variant='h6' className={classes.title} data-testid='app-title'>
          {t('app_title')}
        </Typography>

        {
          authState.token
            ? (
              <>
                <LinkButton to='/home' color='inherit'>
                  Home
                </LinkButton>
                <Button onClick={() => dispatch(logout())} color='inherit'>
                  Logout
                </Button>
              </>
            )
            : (
              <>
                <LinkButton to='/register' color='inherit'>
                  {t('register_title')}
                </LinkButton>
                <LinkButton to='/login' color='inherit'>
                  {t('login_title')}
                </LinkButton>
              </>
            )
        }

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

export const CustomAppBar = withRouter(CustomAppBarComponent)
