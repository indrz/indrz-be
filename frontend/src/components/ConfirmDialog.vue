<template>
  <v-dialog
    v-model="show"
    persistent
    max-width="350"
  >
    <v-card>
      <v-card-title class="break-word">
        {{ message }}
      </v-card-title>
      <v-card-actions>
        <v-spacer />
        <v-btn
          :disabled="busy"
          @click="onConfirmClick"
          color="error darken-1"
          text
        >
          {{ yesText }}
        </v-btn>
        <v-btn
          :loading="busy"
          @click="onCancelClick"
          color="blue darken-1"
          text
        >
          {{ cancelText }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'ConfirmDialog',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    message: {
      type: String,
      default: 'Are you sure?'
    },
    cancelText: {
      type: String,
      default: 'Cancel'
    },
    yesText: {
      type: String,
      default: 'Yes'
    },
    busy: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    onCancelClick () {
      this.$emit('cancelClick');
    },
    onConfirmClick () {
      this.$emit('confirmClick');
    }
  }
}
</script>

<style scoped>

</style>
