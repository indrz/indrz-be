import { defineNuxtPlugin } from '#app'
import { useRootStore } from '~/stores/root'

// Nuxt i18n is now provided by @nuxtjs/i18n.
// This plugin only keeps the Pinia root store locale in sync when callers
// explicitly use the injected `setLocale` helper.
export default defineNuxtPlugin(() => {
  const rootStore = useRootStore()

  return {
    provide: {
      setLocale: (locale) => {
        rootStore.SET_LANG(locale)
      }
    }
  }
})
