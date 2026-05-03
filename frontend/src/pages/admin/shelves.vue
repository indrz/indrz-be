<template>
  <div>
    <v-row>
      <v-col>
        <book-shelf-list />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <shelf-data-list />
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import BookShelfList from '@/components/admin/shelves/BookShelfList'
import ShelfDataList from '@/components/admin/shelves/ShelfDataList'
import { useFloorStore } from '~/stores/floor'
import { useBuildingStore } from '~/stores/building'

definePageMeta({
  layout: 'admin'
})

const floorStore = useFloorStore()
const buildingStore = useBuildingStore()

onMounted(() => {
  Promise.all([
    floorStore.LOAD_FLOORS(),
    buildingStore.LOAD_BUILDINGS()
  ])
})
</script>

<style scoped>
</style>
