import { defineStore } from 'pinia'
import api from '~/util/api'

export const useFloorStore = defineStore('floor', {
  state: () => ({
    floors: [],

    // Current active floor (source of truth for share links, UI, etc.)
    activeFloorLevel: null, // number | null
    activeFloorNum: null // string like "floor_0" | null
  }),

  getters: {
    // IMPORTANT: do NOT name a getter "floors" because it collides with state.floors
    firstFloor: (state) => (state.floors?.length ? state.floors[0].id : null),

    getFloorName: (state) => (id) => {
      const floor = state.floors.find((f) => f.id === id)
      return floor?.short_name ?? String(id)
    },

    currentFloorLevel: (state) => state.activeFloorLevel,
    currentFloorNum: (state) => state.activeFloorNum
  },

  actions: {
    SET_ACTIVE_FLOOR({ floorLevel, floorNum }) {
      if (floorLevel !== undefined) {
        const parsed = Number(floorLevel)
        this.activeFloorLevel = Number.isFinite(parsed) ? parsed : null
      }

      if (floorNum !== undefined) {
        this.activeFloorNum = floorNum ? String(floorNum) : null
      }
    },

    SET_FLOORS(floors) {
      this.floors = floors
    },

    async LOAD_FLOORS() {
      const response = await api.request({ endPoint: 'floor/' })
      const results = response?.data?.results ?? response?.results ?? []
      this.SET_FLOORS(results)
    }
  }
})
