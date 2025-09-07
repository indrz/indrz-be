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
            dark
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
                    outlined
                    rounded
                    small
                    @click="goToBookway"
                  >
                    {{ item.buttonName }}
                  </v-btn>

                  <v-btn
                    v-if="item.title === 'Event Manager'"
                    class="ml-2 mt-5"
                    outlined
                    rounded
                    small
                    @click="goToEventManager"
                  >
                    {{ item.buttonName }}
                  </v-btn>
                  <v-btn
                    v-if="item.title === 'POI Manager'"
                    rounded
                    class="ml-2 mt-5"
                    outlined
                    small
                    @click="goToPoiEditor"
                  >
                    {{ item.buttonName }}
                  </v-btn>
                  <v-btn
                    v-if="item.title === 'Zoneplan'"
                    class="ml-2 mt-5"
                    outlined
                    rounded
                    small
                    @click="goToZoneplanManager"
                  >
                    {{ item.buttonName }}
                  </v-btn>
                </v-card-actions>
              </div>

              <v-avatar
                class="ma-3"
                size="125"
                tile
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

<script>

export default {
  layout: 'admin',
  data: () => ({
    items: [
      {
        color: '#3d78ff',
        title: 'POI Manager',
        artist: 'Manage POI Locations',
        buttonName: 'START POI MANAGER'
      },
      {
        color: '#1F7087',
        src: 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Books_HD_%288314929977%29.jpg/320px-Books_HD_%288314929977%29.jpg',
        title: 'Bookway',
        artist: 'Library Location Information System',
        buttonName: 'START BOOKWAY MANAGER'
      },
      {
        color: '#34b0d5',
        src: 'https://cdn.vuetifyjs.com/images/cards/sunshine.jpg',
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
      }

    ]
  }),
  methods: {
    goToPoiEditor () {
      this.$router.push('/admin/poi');
    },
    goToEventManager () {
      this.$router.push('/admin/events');
    },
    goToBookway () {
      this.$router.push('/admin/shelves');
    },
    goToZoneplanManager () {
      this.$router.push('/admin/zoneplans');
    }
  }

}
</script>
