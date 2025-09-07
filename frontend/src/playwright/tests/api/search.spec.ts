import { expect, test } from '@playwright/test'
const apiBaseUrl = process.env.TEST_BASE_API_URL
const floorUrl = apiBaseUrl + 'floor/'
const searchUrl = apiBaseUrl + 'search/'
const directionsUrl = apiBaseUrl + 'directions/'

test('Get the floor data', async ({ request }) => {
  const floorsRes = await request.get(floorUrl)
  expect(floorsRes.ok()).toBeTruthy()
  var floorsResBody = await floorsRes.json()
  expect(floorsResBody.count).toBe(27)
})

test('Get Aula info 1050812', async ({ request }) => {
  const fromId = 1050812
  const fromSearchRes = await request.get(searchUrl + 'Aula')
  expect(fromSearchRes.ok()).toBeTruthy()
  const fromSearchResBody = await fromSearchRes.json()
  var feature = fromSearchResBody.features.filter(
    (x) => x.properties.id == fromId
  )[0]
  expect(feature.properties.id).toBe(fromId)
  expect(feature.properties.name).toBe('Aula')
  expect(feature.properties.room_code).toBe('AAEG06')
  expect(feature.properties.floor_name).toBe('EG')
  expect(feature.properties.type_name).toBe('Hallway')
})

test('Get Abstellraum Prechtlsaal 1050792 info', async ({ request }) => {
  const toId = 1050792
  const toSearchRes = await request.get(searchUrl + 'Prechtlsaal')
  expect(toSearchRes.ok()).toBeTruthy()
  const toSearchResBody = await toSearchRes.json()
  var feature = toSearchResBody.features.filter(
    (x) => x.properties.id == toId
  )[0]
  expect(feature.properties.id).toBe(1050792)
  expect(feature.properties.name).toBe('Abstellraum Prechtlsaal')
  expect(feature.properties.room_code).toBe('AAEG12')
  expect(feature.properties.floor_name).toBe('EG')
  expect(feature.properties.type_name).toBe('Laboratory')
})

test('API Karlsplatz from Aula to Prechtlsaal search', async ({ request }) => {
  const fromId = 1050812
  const toId = 1050792

  const directionsRes = await request.get(
    directionsUrl +
      `space%3D${fromId}&space%3D${toId}&reversed%3Dfalse&type%3D0`
  )
  expect(directionsRes.ok()).toBeTruthy()
  const directionsResBody = await directionsRes.json()

  const route_length = Number.parseFloat(
    directionsResBody.route_info.route_length
  )
  expect(route_length).toBeGreaterThan(55)
  expect(route_length).toBeLessThan(59)
  const walk_time = Number.parseFloat(directionsResBody.route_info.walk_time)
  expect(walk_time).toBeGreaterThan(39)
  expect(walk_time).toBeLessThan(43)
  expect(directionsResBody.route_info.start_name).toBe(
    'Abstellraum Prechtlsaal'
  )
  expect(directionsResBody.route_info.end_name).toBe('Aula')
})
