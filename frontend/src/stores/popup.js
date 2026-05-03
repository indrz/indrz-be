import { defineStore } from 'pinia'

/**
 * UI-owned popup model for the OpenLayers overlay.
 * Map logic writes data here; Vue components render it.
 * `origin` helps prevent opening the LeftPanel on non-user-triggered events.
 */
export const usePopupStore = defineStore('popup', {
  state: () => ({
    model: null,
    origin: null // 'user' | 'system' | null
  }),

  actions: {
    SET_POPUP(model, origin = 'user') {
      this.model = model
      this.origin = origin
    },
    CLEAR_POPUP() {
      this.model = null
      this.origin = null
    }
  }
})
