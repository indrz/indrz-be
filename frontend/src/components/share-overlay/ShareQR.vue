<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="12" md="12" style="max-width: 220px">
        <v-card flat max-width="220" class="mt-5">
          <div class="share-qr">
            <div class="share-qr-img-container">
              <img ref="shareQrCode" src="" alt="" class="share-qr-img">
            </div>
            <div class="share-qr-logo-container">
              <img src="/images/logo-indrz-with-name.png" alt="indrz logo">
            </div>
          </div>
          <v-row class="mt-1">
            <v-col cols="6" sm="6" md="6">
              <v-btn
                @click="onDownloadButtonClick"
                :loading="isDownloadingQR"
                text
                x-small
              >
                <v-icon small>
                  mdi-download
                </v-icon>
                Download
              </v-btn>
            </v-col>
            <v-col cols="6" sm="6" md="6">
              <v-btn
                @click="onTestLinkButtonClick"
                text
                x-small
              >
                <v-icon small>
                  mdi-share
                </v-icon>
                Test Link
              </v-btn>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import QRCode from 'qrcode';
import { toBlob } from 'html-to-image';
import { getFormattedDate } from '@/util/misc';

export default {
  name: 'ShareQR',
  data () {
    return {
      qrLink: '',
      isDownloadingQR: false
    }
  },
  methods: {
    onDownloadButtonClick () {
      this.isDownloadingQR = true;
      const qrImageArea = document.querySelector('.share-qr');

      toBlob(qrImageArea)
        .then(function (blob) {
          window.saveAs(blob, `QR-location-${getFormattedDate()}.png`);
        })
        .finally(() => {
          this.isDownloadingQR = false;
        });
    },
    onTestLinkButtonClick () {
      window.open(this.qrLink, '_blank');
    },
    setQRCode (link) {
      this.qrLink = link;
      const opts = {
        errorCorrectionLevel: 'H',
        type: 'image/jpeg',
        quality: 0.3,
        margin: 1
      };
      this.$nextTick(() => {
        QRCode.toDataURL(link, opts, (err, url) => {
          if (err) {
            throw err;
          }
          this.$refs.shareQrCode.src = url;
        })
      });
    }
  }
}
</script>

<style lang="scss" scoped>
  .share-qr {
    border: 4px solid black;
    border-radius: 12px !important;
    width: 196px;
    height: 234px;
    background-color: #ffffff;
  }

  .share-qr-img-container {
    margin: 8px;
  }

  .share-qr-img {
    width: 172px;
    height: 172px;
  }

  .share-qr-logo-container {
    margin: 0px auto;
    width: 50px;

    img {
      width: 50px;
    }
  }
</style>
