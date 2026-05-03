import { defineStore } from 'pinia'

export const useRootStore = defineStore('index', {
  state: () => ({
    locales: ['en', 'de'],
    locale: 'en',
    snackBar: ''
  }),

  actions: {
    SET_LANG(locale) {
      if (this.locales.includes(locale)) {
        this.locale = locale
      }
    },
    SET_SNACKBAR(val) {
      this.snackBar = val
    }
  }
})
