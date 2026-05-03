import { defineStore } from 'pinia'
import api from '@/util/api'

const bookShelfEndpoint = 'bookway/bookshelf/'
const shelfDataEndpoint = '/shelfdata/'

const initialShelves = {
  data: [],
  total: 0
}
const initialShelfData = {
  data: [],
  total: 0
}

export const useShelfStore = defineStore('shelf', {
  state: () => ({
    shelves: initialShelves,
    shelfData: initialShelfData,
    selectedShelf: null,
    selectedShelfData: null,
    lastShelfQuery: null
  }),

  actions: {
    setShelves({ data = [], total = 0 }) {
      this.shelves = { data, total }
    },
    setSelectedShelf(shelf) {
      this.selectedShelf = shelf
    },
    setShelfData(shelfData) {
      this.shelfData = shelfData
    },
    setSelectedShelfData(shelfData) {
      this.selectedShelfData = shelfData
    },
    setLastShelfQuery(query) {
      this.lastShelfQuery = query
    },
    async LOAD_BOOKSHELF_LIST(query) {
      const urlWithParams = api.getURLParamsFromPayLoad(query)

      const { data } = await api.request({
        endPoint: `${bookShelfEndpoint}${urlWithParams}`
      })

      const shelfListData = {
        data: data.results.features,
        total: data.count
      }
      this.setLastShelfQuery(query)
      this.setShelves(shelfListData)
      this.setShelfData(initialShelfData)
      this.setSelectedShelf(null)
    },

    async SET_SELECTED_SHELF(shelf) {
      this.setSelectedShelf(shelf)

      if (!shelf) {
        this.setShelfData(initialShelfData)
        return
      }
      const shelfData = await api.request({
        endPoint: `${bookShelfEndpoint}${shelf.id}${shelfDataEndpoint}`
      })

      this.setShelfData(shelfData)
    },
    SET_SELECTED_SHELF_DATA(shelfData) {
      this.setSelectedShelfData(shelfData)
    },

    async SAVE_SHELF(data) {
      let apiRequest = api.postRequest
      let endPoint = bookShelfEndpoint

      if (data.id) {
        apiRequest = api.putRequest
        endPoint = `${bookShelfEndpoint}${data.id}/`
      }

      const response = await apiRequest({
        data: data,
        endPoint
      })

      await this.LOAD_BOOKSHELF_LIST(this.lastShelfQuery)

      return response.data
    },

    async DELETE_SHELF(data) {
      const response = await api.request({
        endPoint: `${bookShelfEndpoint}${data.id}/`,
        method: 'DELETE'
      })

      await this.LOAD_BOOKSHELF_LIST(this.lastShelfQuery)

      return response.data
    },

    async SAVE_SHELF_DATA(data) {
      let apiRequest = api.postRequest
      let endPoint = shelfDataEndpoint

      if (data.id) {
        apiRequest = api.putRequest
        endPoint = `${shelfDataEndpoint}${data.id}/`
      }

      const response = await apiRequest({
        data: data,
        endPoint: `bookway${endPoint}`
      })

      await this.SET_SELECTED_SHELF(this.selectedShelf)

      return response.data
    },

    async DELETE_SHELF_DATA(data) {
      const response = await api.request({
        endPoint: `bookway${shelfDataEndpoint}${data.id}/`,
        method: 'DELETE'
      })

      await this.SET_SELECTED_SHELF(this.selectedShelf)

      return response.data
    }
  }
})
