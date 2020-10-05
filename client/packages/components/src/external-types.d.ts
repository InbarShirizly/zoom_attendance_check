export interface WithTranslateProps {
  i18n: {
    changeLanguage(lang: string): void
  }
  t(key: string): string | undefined | null
}
