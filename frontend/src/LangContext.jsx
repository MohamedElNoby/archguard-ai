import { createContext, useContext, useState, useEffect } from 'react'
import { translations } from './i18n.js'

const LangContext = createContext(null)

/**
 * LangProvider — wraps the entire app.
 * Persists language choice to localStorage so it survives page refresh.
 */
export function LangProvider({ children }) {
  const [lang, setLangState] = useState(
    () => localStorage.getItem('archguard_lang') || 'en'
  )

  const setLang = (l) => {
    setLangState(l)
    localStorage.setItem('archguard_lang', l)
  }

  // Keep <html> dir + lang attributes in sync
  useEffect(() => {
    const dir = lang === 'ar' ? 'rtl' : 'ltr'
    document.documentElement.dir  = dir
    document.documentElement.lang = lang
  }, [lang])

  const value = {
    lang,
    setLang,
    dir: lang === 'ar' ? 'rtl' : 'ltr',
    isRTL: lang === 'ar',
    t: translations[lang],
  }

  return <LangContext.Provider value={value}>{children}</LangContext.Provider>
}

/** Convenience hook — use anywhere inside the tree */
export function useLang() {
  const ctx = useContext(LangContext)
  if (!ctx) throw new Error('useLang must be used inside <LangProvider>')
  return ctx
}
