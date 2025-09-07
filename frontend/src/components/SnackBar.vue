<template>
  <v-snackbar
    v-model="show"
    :timeout="timeout"
    :top="true"
  >
    {{ text }}
    <v-btn
      @click="show = false"
      color="blue"
      text
    >
      Close
    </v-btn>
  </v-snackbar>
</template>

<script>

export default {
  name: 'SnackBar',
  props: {
    timeout: {
      type: Number,
      default: function () {
        return 2000;
      }
    }
  },
  data: function () {
    return {
      show: false,
      text: ''
    };
  },
  created () {
    this.$store.watch(state => state.snackBar, () => {
      const { snackBar } = this.$store.state;

      if (snackBar !== '') {
        this.show = true;
        this.text = snackBar;
        this.$store.commit('SET_SNACKBAR', '');
      }
    });
  }
};
</script>

<style scoped>

</style>
