<template>
  <v-card
    id="floorList"
    :max-height="containerHeight"
    class="mx-auto floor-changer"
  >
    <!-- Desktop/tablet: list with active selection -->
    <v-list
      v-if="!isSmallScreen"
      v-model:selected="selectedIds"
      density="compact"
      selectable
      mandatory
    >
      <v-list-item
        v-for="(floor, i) in floors"
        :key="floor.id ?? i"
        :value="floor.id"
        @click.stop="onFloorClick(floor)"
      >
        <v-list-item-title v-text="floor.short_name" />
      </v-list-item>
    </v-list>

    <!-- Mobile: select dropdown -->
    <div v-else>
      <v-select
        v-model="selectedFloor"
        :items="floors"
        item-title="short_name"
        item-value="id"
        variant="solo"
        density="compact"
        hide-details
        return-object
        @update:model-value="onFloorClick"
      />
    </div>
  </v-card>
</template>

<script setup>
import { computed, ref, watch, onMounted, onUnmounted } from 'vue';
import { useFloorStore } from '~/stores/floor';
import bus from '~/util/bus';

const emit = defineEmits(['floorClick']);

const selectedFloor = ref(null);
const selectedIds = ref([]);

const floorStore = useFloorStore();
const floors = computed(() => {
  const val = floorStore.floors;
  return typeof val === 'function' ? val() : floorStore.$state.floors;
});

const isSmallScreen = computed(() => {
  // Vuetify injected display object is available on component proxy.
  // In setup, access via `useDisplay` would be nicer, but keep minimal change:
  return (getCurrentInstance()?.proxy?.$vuetify?.display?.smAndDown) ?? false;
});

const containerHeight = computed(() => (isSmallScreen.value ? '100px' : '400px'));

function syncSelectionFromFloor(floor) {
  if (!floor || !floor.id) {
    selectedIds.value = [];
    return;
  }
  selectedIds.value = [floor.id];
}

function onFloorClick(floor) {
  if (!floor) return;
  selectedFloor.value = floor;
  syncSelectionFromFloor(floor);
  emit('floorClick', floor);
}

function handleSearchQuery(queryData) {
  const floorNum =
    (queryData?.features?.length && queryData.features[0]?.properties?.floor_num) ||
    (queryData?.type === 'Feature' ? queryData?.properties?.floor_num : null);

  if (typeof floorNum !== 'number' || Number.isNaN(floorNum)) {
    return;
  }

  const found = floors.value.find(f => Number(f.floor_num).toFixed(1) === Number(floorNum).toFixed(1));
  if (found) {
    selectedFloor.value = found;
    syncSelectionFromFloor(found);
    emit('floorClick', found);
  }
}

watch(selectedFloor, (floor) => {
  syncSelectionFromFloor(floor);
});

// Watch the store's activeFloorLevel to sync selection when floor changes from URL or external source
watch(
  () => floorStore.activeFloorLevel,
  (level) => {
    if (level === null || level === undefined) return;
    if (!Array.isArray(floors.value) || !floors.value.length) return;

    // Find the floor matching the active level
    const found = floors.value.find(f => Number(f.floor_num).toFixed(1) === Number(level).toFixed(1));
    if (found && found.id !== selectedFloor.value?.id) {
      selectedFloor.value = found;
      syncSelectionFromFloor(found);
    }
  }
);

watch(
  floors,
  (list) => {
    if (!Array.isArray(list) || !list.length) return;

    // Check if there's already an active floor level set (e.g., from URL parameter)
    const activeLevel = floorStore.activeFloorLevel;
    if (activeLevel !== null && activeLevel !== undefined) {
      const found = list.find(f => Number(f.floor_num).toFixed(1) === Number(activeLevel).toFixed(1));
      if (found) {
        selectedFloor.value = found;
        syncSelectionFromFloor(found);
        return;
      }
    }

    // Default to first floor if no active floor is set
    if (!selectedFloor.value) {
      selectedFloor.value = list[0];
      syncSelectionFromFloor(list[0]);
      // Do not auto-emit click on load; selection UI only.
    }
  },
  { immediate: true }
);

onMounted(() => {
  bus.on('searchResponse', handleSearchQuery);
});

onUnmounted(() => {
  bus.off('searchResponse', handleSearchQuery);
});
</script>

<style scoped lang="scss">
  .floor-changer {
    position: absolute;
    right: 10px;
    top: 70px;
    overflow-y: auto;
    scrollbar-width: none;
    background-color: transparent;
    .v-list-item__title {
      text-align: center;
    }
    .v-list-item__content {
      min-width: 30px;
    }
    .v-select {
      max-width: 100px;
    }
  }
  .v-list-item--active{
    background-color: #0048ff;
  }
  .v-theme--dark .floor-changer {
    background-color: #1E1E1E;
  }
  @-moz-document url-prefix() {
    .floor-changer {
      scrollbar-width: thin;
    }
  }
</style>
