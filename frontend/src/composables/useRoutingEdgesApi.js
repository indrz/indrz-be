// composables/useRoutingEdgesApi.js
import { useNuxtApp } from '#app'

export function useRoutingEdgesApi() {
  const baseUrl = '/api/routing-edges'
  const { $fetch } = useNuxtApp()

  async function fetchEdges(params = {}) {
    const query = new URLSearchParams()
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        query.append(key, String(value))
      }
    })

    const response = await $fetch(`${baseUrl}/?${query.toString()}`, {
      method: 'GET',
    })

    return response && response.features ? response.features : []
  }

  async function bulkSave(payload) {
    const response = await $fetch(`${baseUrl}/bulk-save/`, {
      method: 'POST',
      body: payload,
    })

    if (!response) {
      throw new Error('No response data from bulk-save')
    }
    return response
  }

  return {
    fetchEdges,
    bulkSave,
  }
}
