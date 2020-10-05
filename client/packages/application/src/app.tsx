import React from 'react'
import { render } from 'react-dom'
import i18n from 'i18next'
import { initReactI18next, withTranslation } from 'react-i18next'
import { Application } from 'components'

i18n
  .use(initReactI18next)
  .init({
    resources: {
      en: {
        translation: require('translations/en.json')
      },
      he: {
        translation: require('translations/he.json')
      }
    },
    lng: 'en',
    fallbackLng: 'en',
    debug: true,
    interpolation: {
      escapeValue: false
    }
  })

const AppWithHOCs = withTranslation()(Application)

render(
  <AppWithHOCs />,
  document.getElementById('root')
)
