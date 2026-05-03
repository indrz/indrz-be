<template>
  <v-dialog
    v-model="dialog"
    :max-width="maxWidth"
    persistent
  >
    <v-card>
      <v-card-title class="text-h5">
        {{ title }}
      </v-card-title>
      <v-card-text>
        {{ message }}
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn
          variant="text"
          @click="cancel"
        >
          {{ cancelText || $t('cancel') }}
        </v-btn>
        <v-btn
          :color="confirmColor"
          variant="elevated"
          @click="confirm"
        >
          {{ confirmText || $t('confirm') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'ConfirmDialog',
  data () {
    return {
      dialog: false,
      title: '',
      message: '',
      confirmText: '',
      cancelText: '',
      confirmColor: 'primary',
      maxWidth: 400,
      resolvePromise: null,
      rejectPromise: null
    };
  },
  methods: {
    open (title, message, options = {}) {
      this.dialog = true;
      this.title = title;
      this.message = message;
      this.confirmText = options.confirmText || '';
      this.cancelText = options.cancelText || '';
      this.confirmColor = options.confirmColor || 'primary';
      this.maxWidth = options.maxWidth || 400;

      return new Promise((resolve, reject) => {
        this.resolvePromise = resolve;
        this.rejectPromise = reject;
      });
    },
    confirm () {
      this.dialog = false;
      if (this.resolvePromise) {
        this.resolvePromise(true);
      }
    },
    cancel () {
      this.dialog = false;
      if (this.rejectPromise) {
        this.rejectPromise(false);
      }
    }
  }
};
</script>