<template>
  <v-app id="admin-app">
    <side-bar
      v-if="isUserSignedIn"
      :menu-items="menuItems"
      :drawer="drawer"
      @drawerClick="onDrawerClick"
    />
    <v-app-bar
      v-if="isUserSignedIn"
      app
      color="indigo"
      density="compact"
      prominent
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-toolbar-title>INDRZ MANAGER</v-toolbar-title>
      <v-spacer />
      <user-menu />
    </v-app-bar>
    <v-main>
      <v-container :class="isPoiManager ? 'admin-map-container' : 'pages'">
        <NuxtPage />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import SideBar from '../components/admin/SideBar'
import UserMenu from '../components/admin/UserMenu'
import { useUserStore } from '~/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const drawer = ref(null)
const menuItems = [
  {
    text: 'Dashboard',
    icon: 'home',
    route: { name: '', path: '/admin/' }
  },
  {
    text: 'Bookway Editor',
    icon: 'book-open-blank-variant',
    route: { name: 'shelves', path: '/admin/shelves' }
  },
  {
    text: 'POI Manager',
    icon: 'map-marker',
    route: { name: 'poi', path: '/admin/poi' }
  },
  {
    text: 'Zoneplan',
    icon: 'floor-plan',
    route: { name: 'zoneplans', path: '/admin/zoneplans' }
  },
  {
    text: 'BETA, Event Manager',
    icon: 'party-popper',
    route: { name: 'events', path: '/admin/events' }
  }
]

const isUserSignedIn = computed(() => userStore.isUserSignedIn)

const isPoiManager = computed(() => {
  return ['admin-poi', 'admin-poi-editor'].includes(route.name)
})

watch(isUserSignedIn, (value) => {
  if (!value) {
    router.push(route.query.redirect || '/admin/login')
  }
})

function onDrawerClick (drawerValue) {
  drawer.value = drawerValue
}
</script>
<style scoped>
  .admin-map-container {
    align-items: start;
    width: 100%;
    height: 100%;
    padding: 0px !important;
    margin: 0px !important;
    padding: 0px !important;
    max-width: none;
  }
</style>
