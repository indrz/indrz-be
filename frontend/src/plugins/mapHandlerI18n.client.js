import { defineNuxtPlugin } from '#app'
import mapHandler from '~/util/mapHandler'

export default defineNuxtPlugin((nuxtApp) => {
  // Ensure mapHandler always has a working i18n `t()` function.
  // This avoids scattered `mapHandler.setI18n(...)` calls across pages/layouts.
  mapHandler.setI18n(nuxtApp.$i18n)
})
