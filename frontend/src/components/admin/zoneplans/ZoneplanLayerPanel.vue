<template>
  <v-list>
    <v-toolbar
      color="purple"
      theme="dark"
    >
      <v-icon>mdi-layers</v-icon>
      <v-toolbar-title>Map Layers</v-toolbar-title>
      <v-spacer />
    </v-toolbar>
    <v-list-group no-action prepend-icon="mdi-office-building">
      <template #activator="{ props }">
        <v-list-item v-bind="props">
          <v-list-item-title>Organization</v-list-item-title>
        </v-list-item>
      </template>

      <v-list-item v-for="org in organizations" :key="org.id" link density="compact">
        <template #prepend>
          <v-checkbox :model-value="org.active" @update:model-value="toggleLayer(org)" />
        </template>
        <v-list-item-title v-text="org.orgcode" />
        <v-list-item-subtitle v-text="org.name" />
        <template #append>
          <v-icon :color="org.color" v-text="org.icon" />
        </template>
      </v-list-item>
    </v-list-group>
    <v-list-group no-action prepend-icon="mdi-office-building">
      <template #activator="{ props }">
        <v-list-item v-bind="props">
          <v-list-item-title>MainuseItems</v-list-item-title>
        </v-list-item>
      </template>

      <v-list-item v-for="mainuse in mainuseCategories" :key="mainuse.id" link density="compact">
        <template #prepend>
          <v-checkbox :model-value="mainuse.active" @update:model-value="toggleMainUseLayer(mainuse)" />
        </template>
        <v-list-item-title v-text="mainuse.name" />
        <template #append>
          <v-icon :color="mainuse.color" v-text="mainuse.icon" />
        </template>
      </v-list-item>
    </v-list-group>
  </v-list>
</template>

<script>
// Import fetch organization codes function
import { fetchOrganizationCodes, fetchMainuseCategories } from '@/util/adminApi'

export default {
  data: () => ({
    organizations: [],
    mainuseCategories: []
  }),

  // Fetch organization codes when component is created
  async created () {
    const organizations = await fetchOrganizationCodes();
    const mainuseCategories = await fetchMainuseCategories();
    this.organizations = organizations;
    this.mainuseCategories = mainuseCategories;
  },
  mounted () { },
  methods: {
    toggleLayer (layer) {
      layer.active = !layer.active;
      this.$emit('layer-toggled', { name: layer.name, orgcode: layer.orgcode, active: layer.active, color: layer.color });
    },
    toggleMainUseLayer (layer) {
      layer.active = !layer.active;
      this.$emit('layer-mainuse-toggled', { name: layer.name, active: layer.active, color: layer.color });
    }
  }

}
</script>
<style scoped>
.label_align {
  text-align: left;
}
</style>
