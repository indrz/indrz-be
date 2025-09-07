<template>
  <v-dialog
    v-model="dialog"
    max-width="400"
  >
    <v-card>
      <v-card-title class="headline" />
      <v-card-text>
        <div v-if="!error">
          <qrcode-stream :camera="camera" @decode="onDecode" @init="onInit" />
        </div>
        <div v-if="error">
          <span class="subtitle-1">{{ locale.cameraFallbackMessage }}</span>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn
          @click="emitCloseEvent"
          text
        >
          Close
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { QrcodeStream } from 'vue-qrcode-reader';

export default {
  name: 'QRCode',
  components: {
    QrcodeStream
  },
  props: {
    show: {
      type: Boolean,
      default: function () {
        return false
      }
    }
  },
  data () {
    return {
      camera: 'off',
      error: false,
      locale: {
        cameraFallbackMessage: this.$t('qr_camera_fallback_message')
      }
    }
  },
  computed: {
    dialog: {
      get: function () {
        return this.show;
      },
      set: function (newValue) {
        this.emitCloseEvent(newValue);
      }
    }
  },
  watch: {
    show: function (newValue) {
      if (newValue && this.camera !== 'auto') {
        this.turnCameraOn();
      } else {
        this.turnCameraOff();
      }
    }
  },
  methods: {
    onDecode (decodedString) {
      if (decodedString && decodedString.includes('?')) {
        this.$emit('qrCodeScanned', decodedString.split('?')[1]);
        this.emitCloseEvent();
      } else {
        this.error = true;
      }
      this.turnCameraOff();
    },
    turnCameraOn () {
      this.camera = 'auto';
      this.error = false;
    },
    turnCameraOff () {
      this.camera = 'off';
    },
    emitCloseEvent () {
      this.$emit('qrCodeShow', false);
    },
    async onInit (promise) {
      try {
        await promise
      } catch (error) {
        let errorMessage = '';

        switch (error.name) {
          case 'NotAllowedError':
            errorMessage = 'ERROR: you need to grant camera access permisson';
            break;
          case 'NotFoundError':
            errorMessage = 'ERROR: no camera on this device';
            break;
          case 'NotSupportedError':
            errorMessage = 'ERROR: secure context required (HTTPS, localhost)';
            break;
          case 'NotReadableError':
            errorMessage = 'ERROR: is the camera already in use?';
            break;
          case 'OverconstrainedError':
            errorMessage = 'ERROR: installed cameras are not suitable';
            break;
          case 'StreamApiNotSupportedError':
            errorMessage = 'ERROR: Stream API is not supported in this browser';
            break;
        }
        alert(errorMessage);
        this.error = true;
        // this.emitCloseEvent();
      }
    }
  }
}
</script>

<style scoped>

</style>
