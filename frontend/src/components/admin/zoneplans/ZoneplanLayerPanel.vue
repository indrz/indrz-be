<template>
  <v-list>
    <v-toolbar
      color="purple"
      dark
    >
      <v-icon>mdi-layers</v-icon>
      <v-spacer>
        <v-toolbar-title>Map Layers</v-toolbar-title>
      </v-spacer>
    </v-toolbar>
    <v-list-group no-action prepend-icon="mdi-office-building">
      <template v-slot:activator>
        <v-list-item-content>
          <v-list-item-title>Organization</v-list-item-title>
        </v-list-item-content>
      </template>

      <v-list-item v-for="org in organizations" :key="org.id" link dense>
        <v-list-item-action>
          <v-checkbox :value="org.active" @change="toggleLayer(org)" />
        </v-list-item-action>
        <!-- Wrap the title and subtitle in v-list-item-content -->
        <v-list-item-content>
          <v-list-item-title v-text="org.orgcode" />
          <v-list-item-subtitle v-text="org.name" />
        </v-list-item-content>

        <v-list-item-icon>
          <v-icon :color="org.color" v-text="org.icon" />
        </v-list-item-icon>
      </v-list-item>
    </v-list-group>
    <v-list-group no-action prepend-icon="mdi-office-building">
      <template v-slot:activator>
        <v-list-item-content>
          <v-list-item-title>MainuseItems</v-list-item-title>
        </v-list-item-content>
      </template>

      <v-list-item v-for="mainuse in mainuseCategories" :key="mainuse.id" link dense>
        <v-list-item-action>
          <v-checkbox :value="mainuse.active" @change="toggleMainUseLayer(mainuse)" />
        </v-list-item-action>
        <!-- Wrap the title and subtitle in v-list-item-content -->
        <v-list-item-content>
          <v-list-item-title v-text="mainuse.name" />
        </v-list-item-content>

        <v-list-item-icon>
          <v-icon :color="mainuse.color" v-text="mainuse.icon" />
        </v-list-item-icon>
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
