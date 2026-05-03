import { defineStore } from 'pinia'
import api from '~/util/api'

const categoryEndpoint = 'poi/category/'

export const usePoiStore = defineStore('poi', {
  state: () => ({
    poiData: [],
    poiIcons: []
  }),

  getters: {
    findNode: (state) => (nodeId) => {
      return findNode(Number.parseInt(nodeId), state.poiData)
    }
  },

  actions: {
    SET_POI(poiData) {
      this.poiData = poiData
    },
    SET_POI_ICONS(poiIcons) {
      this.poiIcons = poiIcons
    },
    async LOAD_POI() {
      const response = await api.request({
        endPoint: 'poi/tree/'
      })
      this.SET_POI(response.data)
    },
    async LOAD_POI_ICONS() {
      const response = await api.request({
        endPoint: 'poi/icon/'
      })
      this.SET_POI_ICONS(response.data.results)
    },
    async GET_POI_CATGORY(_, id) {
      const response = await api.request({
        endPoint: `${categoryEndpoint}${id}/`
      })
      return response.data
    },
    async DELETE_POI_CATGORY(_, id) {
      const response = await api.postRequest({
        endPoint: `${categoryEndpoint}${id}/`,
        method: 'DELETE',
        data: {}
      })

      await this.LOAD_POI()
      return response.data
    },
    async SAVE_POI_CATEGORY(_, data) {
      let apiRequest = api.postRequest
      let endPoint = categoryEndpoint

      if (data.id) {
        apiRequest = api.putRequest
        endPoint = `${categoryEndpoint}${data.id}/`
      }

      const response = await apiRequest({
        data: data,
        endPoint
      })

      await this.LOAD_POI()

      return response
    }
  }
})

const findNode = (nodeId, poiData) => {
  let foundData = null

  poiData.some((d) => {
    if (d.id && d.id === nodeId) {
      foundData = d
      return true
    }
    if (d.children) {
      foundData = findNode(nodeId, d.children)
      if (foundData) {
        if (!foundData.roots) {
          foundData = {
            data: foundData,
            roots: [d.id]
          }
        } else {
          foundData.roots.push(d.id)
        }
        return true
      }
    }
    return false
  })
  return foundData
}
