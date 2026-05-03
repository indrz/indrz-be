<template>
  <div class="poi-page">
    <v-container class="pa-15">
      <v-row
        class="fill-height"
        align="center"
        justify="center"
      >
        <template v-for="(menuItem, i) in menuItems" :key="i">
          <v-col
            cols="12"
            md="4"
          >
            <v-hover v-slot="{ hover }">
              <v-card
                :elevation="hover ? 12 : 2"
                :class="{ 'on-hover': hover }"
                @click="onPoiMenuClick(menuItem.route)"
              >
                <v-card-title class="justify-center">
                  <v-icon
                    size="large"
                    start
                  >
                    mdi-pencil
                  </v-icon>
                  <span class="text-h6 font-weight-light" />

                  {{ menuItem.text }}
                </v-card-title>
              </v-card>
            </v-hover>
          </v-col>
        </template>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'admin'
})

const router = useRouter()
const route = useRoute()

const menuItems = [
  {
    text: 'POI Editor',
    route: { name: 'poi-editor', path: '/admin/poi/editor' }
  },
  {
    text: 'POI Categories',
    route: { name: 'poi-categories', path: '/admin/poi/categories' }
  },
  {
    text: 'POI Icons',
    route: { name: 'poi-icons', path: '/admin/poi/icons' }
  }
]

function onPoiMenuClick (menuRoute) {
  if (menuRoute && menuRoute.path && menuRoute.path !== route.path) {
    router.push(menuRoute.path)
  }
}
</script>

<style scoped>
  .poi-page {
    height: 100%;
    width: 100%;
    background: linear-gradient(180deg, rgba(2,0,36,1) 0%, rgba(9,9,121,1) 35%, rgba(0,212,255,1) 100%);
  }
</style>
