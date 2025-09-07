<template>
  <v-container>
    <v-row no-gutters>
      <v-col cols="9" sm="10" md="10">
        <v-text-field ref="linkField" :value="link" hide-details outlined />
      </v-col>
      <v-col
        cols="3"
        sm="2"
        md="2"
        align="end"
        class="pt-2"
      >
        <v-btn @click="onCopyButtonClick('linkField')" color="blue darken-1" text class="pa-0">
          <v-icon dark>
            mdi-content-copy
          </v-icon>
          {{ copy }}
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'CopyField',
  props: {
    link: {
      type: String,
      default: ''
    }
  },
  data () {
    return {
      copy: this.$t('copy')
    }
  },
  methods: {
    onCopyButtonClick (fieldRef) {
      const copyTextField = this.$refs[fieldRef];
      const inputField = copyTextField.$el.querySelector('input');
      inputField.select();
      inputField.setSelectionRange(0, 99999);
      document.execCommand('copy');
      this.$emit('share-copy');
    }
  }
}
</script>

<style scoped>

</style>
