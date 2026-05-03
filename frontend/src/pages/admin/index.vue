<template>
  <v-card
    max-width="400"
    class="mx-auto"
  >
    <v-container>
      <v-row dense>
        <v-col
          v-for="(item, i) in items"
          :key="i"
          cols="12"
        >
          <v-card
            :color="item.color"
            theme="dark"
          >
            <div class="d-flex flex-no-wrap justify-space-between">
              <div>
                <v-card-title
                  class="text-h5"
                  v-text="item.title"
                />

                <v-card-subtitle v-text="item.artist" />

                <v-card-actions>
                  <v-btn
                    v-if="item.title === 'Bookway'"
                    class="ml-2 mt-3"
                    variant="outlined"
                    rounded
                    size="small"
                    @click="goToBookway"
                  >
                    {{ item.buttonName }}
                  </v-btn>

                  <v-btn
                    v-if="item.title === 'Event Manager'"
                    class="ml-2 mt-5"
                    variant="outlined"
                    rounded
                    size="small"
                    @click="goToEventManager"
                  >
                    {{ item.buttonName }}
                  </v-btn>
                  <v-btn
                    v-if="item.title === 'POI Manager'"
                    rounded
                    class="ml-2 mt-5"
                    variant="outlined"
                    size="small"
                    @click="goToPoiEditor"
                  >
                    {{ item.buttonName }}
                  </v-btn>
                  <v-btn
                    v-if="item.title === 'Route Editor'"
                    class="ml-2 mt-5"
                    variant="outlined"
                    rounded
                    size="small"
                    @click="goToRouteEditor"
                  >
                    {{ item.buttonName }}
                  </v-btn>
                  <v-btn
                    v-if="item.title === 'NEW Route Editor'"
                    class="ml-2 mt-5"
                    variant="outlined"
                    rounded
                    size="small"
                    @click="goToRouteEditorNew"
                  >
                    {{ item.buttonName }}
                  </v-btn>
                  <v-btn
                    v-if="item.title === 'Zoneplan'"
                    class="ml-2 mt-5"
                    variant="outlined"
                    rounded
                    size="small"
                    @click="goToZoneplanManager"
                  >
                    {{ item.buttonName }}
                  </v-btn>
                </v-card-actions>
              </div>

              <v-avatar
                class="ma-3"
                size="125"
                rounded="0"
              >
                <v-img :src="item.src" alt="iamge item source" />
              </v-avatar>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<script setup>
definePageMeta({
  layout: 'admin'
})

const router = useRouter()

const items = [
  {
    color: '#3d78ff',
    src: 'https://cdn.vuetifyjs.com/docs/images/cards/purple-flowers.jpg',
    title: 'POI Manager',
    artist: 'Manage POI Locations',
    buttonName: 'START POI MANAGER'
  },
  {
    color: '#1F7087',
    src: 'https://cdn.vuetifyjs.com/images/cards/sunshine.jpg',
    title: 'Bookway',
    artist: 'Library Location Information System',
    buttonName: 'START BOOKWAY MANAGER'
  },
  {
    color: '#34b0d5',
    src: ' ',
    title: 'Zoneplan',
    artist: 'Organization Zoneplans',
    buttonName: 'OPEN Zoneplans'
  },
  {
    color: '#952175',
    src: 'https://cdn.vuetifyjs.com/images/cards/halcyon.png',
    title: 'Event Manager',
    artist: 'Locations for Events',
    buttonName: 'START EVENT MANAGER'
  },
  {
    color: '#3c87dd',
    src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg',
    title: 'Route Editor',
    artist: 'Edit Routes',
    buttonName: 'START ROUTE EDITOR'
  },
  {
    color: '#3c87dd',
    src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg',
    title: 'NEW Route Editor',
    artist: 'Edit Routes',
    buttonName: 'LAUNCH NEW ROUTE EDITOR'
  }
]

function goToPoiEditor () {
  router.push('/admin/poi')
}
function goToEventManager () {
  router.push('/admin/events')
}
function goToBookway () {
  router.push('/admin/shelves')
}
function goToZoneplanManager () {
  router.push('/admin/zoneplans')
}
function goToRouteEditor () {
  router.push('/admin/map')
}
function goToRouteEditorNew () {
  router.push('/admin/route-editor')
}
</script>
