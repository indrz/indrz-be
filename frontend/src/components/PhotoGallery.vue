<template>
  <v-dialog
    v-model="dialog"
    max-width="1980"
  >
    <v-card>
      <v-toolbar
        elevation="0"
      >
        <v-spacer />
        <v-btn
          icon="mdi-close"
          variant="text"
          @click="dialog = false"
        />
      </v-toolbar>
      <v-card-text class="pa-0">
        <v-carousel v-model="carouselModel" height="80vh">
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
      default: false
    },
    images: {
      type: Array,
      default: () => []
    },
    selctedIndex: {
      type: Number,
      default: 0
    }
  },
  emits: ['gallery:show'],
  data () {
    return {
      items: [
        { src: 'https://placehold.co/600x400'},
        { src: 'https://via.placeholder.com/1920x1080' },
        { src: 'https://via.placeholder.com/1920x1080' }
      ],
      carouselModel: this.selctedIndex
    }
  },
  watch: {
    selctedIndex (newIndex) {
      this.carouselModel = newIndex
    },
    show (isOpen) {
      if (isOpen) {
        this.carouselModel = this.selctedIndex
      }
    }
  },
  computed: {
    dialog: {
      get () {
        return this.show;
      },
      set (newValue) {
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
