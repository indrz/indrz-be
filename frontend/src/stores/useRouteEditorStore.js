// stores/useRouteEditorStore.js
import { defineStore } from 'pinia'
import { useRoutingEdgesApi } from '~/composables/useRoutingEdgesApi'

export const useRouteEditorStore = defineStore('routeEditor', {
  state: () => ({
    campusId: null,
    buildingId: null,
    floorId: null,
    edges: [],
    created: [],
    updated: [],
    deleted: [],
    isLoading: false,
    lastError: null
  }),

  getters: {
    isDirty(state) {
      return (
        state.created.length > 0 ||
        state.updated.length > 0 ||
        state.deleted.length > 0
      )
    }
  },

  actions: {
    setContext(campusId, buildingId, floorId) {
      this.campusId = campusId
      this.buildingId = buildingId
      this.floorId = floorId
    },

    async loadEdges() {
      if (!this.campusId || !this.buildingId || !this.floorId) return
      this.isLoading = true
      this.lastError = null
      try {
        const api = useRoutingEdgesApi()
        const features = await api.fetchEdges({
          campus: this.campusId,
          building: this.buildingId,
          floor_from: this.floorId
        })
        this.edges = features
        this.created = []
        this.updated = []
        this.deleted = []
      } catch (err) {
        this.lastError = err && err.message ? err.message : 'Failed to load edges'
      } finally {
        this.isLoading = false
      }
    },

    addCreatedEdge(edge) {
      this.created.push(edge)
    },

    markUpdatedEdge(edge) {
      const existingIdx = this.updated.findIndex((e) => e.id === edge.id)
      if (existingIdx >= 0) {
        this.updated[existingIdx] = { ...this.updated[existingIdx], ...edge }
      } else {
        this.updated.push(edge)
      }
    },

    markDeletedEdge(edgeId) {
      if (!this.deleted.some((e) => e.id === edgeId)) {
        this.deleted.push({ id: edgeId })
      }
      this.created = this.created.filter((c) => c.temp_id !== String(edgeId))
      this.updated = this.updated.filter((u) => u.id !== edgeId)
    },

    clearChanges() {
      this.created = []
      this.updated = []
      this.deleted = []
    },

    updateEdgePropertiesLocally(edgeId, updates) {
      const idx = this.edges.findIndex((f) => f.id === edgeId)
      if (idx === -1) return
      const feature = this.edges[idx]
      const newProps = {
        ...(feature.properties || {}),
        ...updates
      }
      this.edges[idx] = {
        ...feature,
        properties: newProps
      }
    },

    async saveChanges() {
      if (!this.campusId || !this.buildingId) return
      this.isLoading = true
      this.lastError = null

      try {
        const api = useRoutingEdgesApi()
        const response = await api.bulkSave({
          campus: this.campusId,
          building: this.buildingId,
          created: this.created,
          updated: this.updated,
          deleted: this.deleted
        })

        await this.loadEdges()
        this.created = []
        this.updated = []
        this.deleted = []
        return response
      } catch (err) {
        this.lastError = err && err.message ? err.message : 'Failed to save changes'
        throw err
      } finally {
        this.isLoading = false
      }
    }
  }
})
