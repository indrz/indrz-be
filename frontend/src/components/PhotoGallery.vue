<template>
  <v-dialog
    v-model="dialog"
    max-width="1980"
  >
    <v-card>
      <v-toolbar
        flat
      >
        <v-spacer />
        <v-btn
          icon
          @click="dialog = false"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-toolbar>
      <v-card-text class="pa-0" style="">
        <v-carousel :value="selctedIndex" class="" height="80vh">
          <v-carousel-item v-for="(image, i) in images" :key="i">
            <div class="image-wrapper">
              <img :src="`${baseUrl}${image.image}`" :alt="image.alt_text" class="image">
            </div>
          </v-carousel-item>
        </v-carousel>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import config from '@/util/indrzConfig'

const { env } = config;

export default {
  name: 'PhotoGallery',

  props: {
    show: {
      type: Boolean,
      default: function () {
        return false;
      }
    },
    images: {
      type: Array,
      default: function () {
        return [];
      }
    },
    selctedIndex: {
      type: Number,
      default: function () {
        return 0;
      }
    }
  },
  data () {
    return {
      items: [
        { src: 'https://via.placeholder.com/1920x1080' },
        { src: 'https://via.placeholder.com/1920x1080' },
        { src: 'https://via.placeholder.com/1920x1080' }
      ]
    }
  },
  computed: {
    dialog: {
      get: function () {
        return this.show;
      },
      set: function (newValue) {
        this.$emit('gallery:show', newValue);
      }
    },
    baseUrl () {
      return env.BASE_URL
    }
  }
};
</script>

<style scoped>
.image-wrapper {
  width: 100%;
  height: 100%;
  overflow: auto;
  display: grid;
  justify-content: center;
  align-items: center;
}

.image {
  width: 100%;
}
</style>
