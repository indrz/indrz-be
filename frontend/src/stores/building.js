import { defineStore } from 'pinia'
import api from '@/util/api'

export const useBuildingStore = defineStore('building', {
  state: () => ({
    buildings: [],
    currentBuildingId: null,
    floors: []
  }),

  getters: {
    firstBuilding: (state) => () => {
      return state.buildings && state.buildings.length ? state.buildings[0].id : null
    },
    firstFloor: (state) => () => {
      return state.floors && state.floors.length ? state.floors[0].id : null
    },
    getBuildingName: (state) => (id) => {
      let name = ''
      try {
        const building = state.buildings.find((building) => building.id === id)

        if (building) {
          name = building.properties.building_name
        }
      } catch (err) {
        console.log(err)
      }
      return name || id
    },
    getFloorName: (state) => (id) => {
      let name = ''
      const floor = state.floors.find((floor) => floor.id === id)

      if (floor) {
        name = floor.short_name
      }
      return name || id
    }
  },

  actions: {
    SET_BUILDINGS(buildings) {
      this.buildings = buildings
    },
    SET_CURRENT_BUILDING(buildingId) {
      this.currentBuildingId = buildingId
    },
    SET_FLOORS(floors) {
      this.floors = floors
    },
    async LOAD_BUILDINGS() {
      const response = await api.request({
        endPoint: 'buildings/'
      })
      this.SET_BUILDINGS(response?.data?.results?.features || [])
    },
    async LOAD_FLOORS(buildingId) {
      let idToLoad = buildingId
      if (!idToLoad) {
        idToLoad = this.firstBuilding()
      }

      if (idToLoad === this.currentBuildingId) {
        return
      }
      this.SET_CURRENT_BUILDING(idToLoad)
      const response = await api.request({
        endPoint: `buildings/${idToLoad}/floors/`
      })
      this.SET_FLOORS(response?.data || [])
    }
  }
})
