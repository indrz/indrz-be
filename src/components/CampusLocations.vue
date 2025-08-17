<template>
  <div>
    <div class="text-center">
      <v-progress-circular
        v-if="loading"
        indeterminate
        color="primary"
      />
    </div>

    <v-list v-if="!loading" dense nav>
      <v-list-item-group color="primary">
        <v-list-item
          v-for="(campus, i) in campusLocations"
          :key="i"
          @click.stop="onLocationClick(campus, 16)"
        >
          <v-list-item-content>
            <v-list-item-title v-text="campus.name" />
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>
  </div>
</template>

<script>
import api from '../util/api';

export default {
  name: 'CampusLocations',
  data: () => ({
    loading: true,
    campusLocations: []
  }),

  async mounted () {
    const locationsData = await this.fetchLocations();

    if (locationsData && locationsData.data && locationsData.data.results) {
      this.campusLocations = locationsData.data.results;
    }
    this.loading = false;
  },

  methods: {
    onLocationClick (location, zoom) {
      this.$emit('locationClick', location.centroid, zoom);
    },
    fetchLocations () {
      return api.request({
        endPoint: 'campus/'
      }, {
        baseApiUrl: process.env.BASE_API_URL,
        token: process.env.TOKEN
      });
    }
  }
};
</script>
