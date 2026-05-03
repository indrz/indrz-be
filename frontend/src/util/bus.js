const listeners = new Map()

const on = (event, handler) => {
  if (!event || typeof handler !== 'function') {
    return
  }
  if (!listeners.has(event)) {
    listeners.set(event, new Set())
  }
  listeners.get(event).add(handler)
}

const off = (event, handler) => {
  const handlers = listeners.get(event)
  if (!handlers) {
    return
  }
  handlers.delete(handler)
  if (handlers.size === 0) {
    listeners.delete(event)
  }
}

const emit = (event, payload) => {
  const handlers = listeners.get(event)
  if (!handlers) {
    return
  }
  // Copy to avoid issues if handlers modify subscriptions
  Array.from(handlers).forEach((handler) => {
    try {
      handler(payload)
    } catch (error) {
      // eslint-disable-next-line no-console
      console.error(error)
    }
  })
}

export default {
  on,
  off,
  emit
}

