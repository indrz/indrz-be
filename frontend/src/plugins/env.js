import { defineNuxtPlugin, useRuntimeConfig } from '#app'
import config from '../util/indrzConfig'

export default defineNuxtPlugin(() => {
  const runtimeConfig = useRuntimeConfig()
  const mergedEnv = {
    ...(runtimeConfig.public || {})
  }

  const parseNumber = (value) => {
    if (typeof value === 'number') return value
    if (typeof value !== 'string') return value
    const parsed = Number(value)
    return Number.isFinite(parsed) ? parsed : value
  }

  const parseNumberArray = (value) => {
    if (Array.isArray(value)) {
      return value.map(parseNumber)
    }
    if (typeof value !== 'string') return value
    const trimmed = value.trim()
    if (!trimmed) return value

    if (trimmed.startsWith('[') && trimmed.endsWith(']')) {
      try {
        const parsed = JSON.parse(trimmed)
        if (Array.isArray(parsed)) {
          return parsed.map(parseNumber)
        }
      } catch (error) {
        // Fall through to comma parsing.
      }
    }

    const parts = trimmed.replace(/^\[|\]$/g, '').split(',')
    const numbers = parts.map((part) => Number(part.trim())).filter((num) => Number.isFinite(num))
    return numbers.length >= 2 ? numbers : value
  }

  const parsedEnv = {
    ...mergedEnv,
    DEFAULT_CENTER_XY: parseNumberArray(mergedEnv.DEFAULT_CENTER_XY),
    MOBILE_START_CENTER_XY: parseNumberArray(mergedEnv.MOBILE_START_CENTER_XY),
    DEFAULT_START_ZOOM: parseNumber(mergedEnv.DEFAULT_START_ZOOM),
    MOBILE_START_ZOOM: parseNumber(mergedEnv.MOBILE_START_ZOOM),
    DEFAULT_START_FLOOR: parseNumber(mergedEnv.DEFAULT_START_FLOOR)
  }

  const resolvedToken = runtimeConfig.TOKEN || runtimeConfig.public?.TOKEN
  if (resolvedToken) {
    parsedEnv.TOKEN = resolvedToken
  }

  config.set(parsedEnv)

  if (typeof globalThis.process === 'undefined') {
    globalThis.process = { env: parsedEnv }
  } else {
    globalThis.process.env = { ...(globalThis.process.env || {}), ...parsedEnv }
  }

  return {
    provide: {
      env: parsedEnv
    }
  }
})
