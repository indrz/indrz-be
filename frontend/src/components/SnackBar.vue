<template>
  <v-snackbar
    v-model="snackbar"
    :timeout="timeout"
    :color="color"
    :location="location"
    :multi-line="multiLine"
  >
    {{ text }}
    <template #actions>
      <v-btn
        variant="text"
        @click="snackbar = false"
      >
        {{ $t('close') }}
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
export default {
  name: 'SnackBar',
  data () {
    return {
      snackbar: false,
      text: '',
      timeout: 3000,
      color: 'info',
      location: 'top',
      multiLine: false
    };
  },
  methods: {
    show (message, options = {}) {
      this.text = message;
      this.timeout = options.timeout || 3000;
      this.color = options.color || 'info';
      this.location = options.location || 'top';
      this.multiLine = options.multiLine || false;
      this.snackbar = true;
    }
  }
};
</script>

<style scoped>

</style>
