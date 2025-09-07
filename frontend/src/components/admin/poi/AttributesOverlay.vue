<template>
  <v-dialog
    v-model="isVisible"
    :width="dialogWidth"
    :style="{'min-width': popupSize.width}"
    persistent
  >
    <v-card flat>
      <v-toolbar
        dense
        flat
        height="24"
      >
      <v-title class="headline pa-5">
        POI EDIT FORM
      </v-title>
        <v-spacer />
        <v-btn icon @click="onCloseClick">
          <v-icon>mdi-window-close</v-icon>
        </v-btn>
      </v-toolbar>
      <v-card-text class="pa-5">
        <v-form
          ref="form"
          v-model="valid"
          dense
          lazy-validation
        >
          <v-container class="pa-0">
            <v-row no-gutters>
              <v-col>
                <v-text-field v-model="data.name" :rules="requiredRule" label="name" />
                <v-text-field v-model="data.name_en" label="name-en" />
                <v-text-field v-model="data.name_de" label="name-de" />
                <v-textarea
                  v-model="data.html_content"
                  label="HTML Content"
                  rows="3"
                  no-resize
                  row-height="25"
                />
                <v-checkbox
                  v-model="data.enabled"
                  label="enabled"
                  hide-details
                  dense
                />
                <v-file-input
                  ref="uploadImage"
                  v-model="imageFile"
                  multiple
                  accept="image/*"
                  label="Click here to upload Image"
                  show-size
                  :rules="imageUploadRules"
                  prepend-icon=""
                  append-icon="mdi-plus"
                  :disabled="isLoading"
                  @change="onImageUpload"
                  @click:append="selectFile"
                />
                <div v-if="!feature && imageFiles.length" class="pending-images">
                  <v-list dense style="max-height: 120px" class="overflow-y-auto">
                    <div v-for="(file, index) in imageFiles" :key="index">
                      <v-list-item class="pl-0">
                        <v-alert
                          color="info"
                          class="white--text text-center pa-1 ma-0"
                          width="100%"
                          v-text="file.name"
                        />
                        <v-list-item-action>
                          <v-btn icon x-small @click="removeSelectedImage(index)">
                            <v-icon color="error darken-1">mdi-delete</v-icon>
                          </v-btn>
                        </v-list-item-action>
                      </v-list-item>
                    </div>
                  </v-list>
                </div>
                <v-list
                  dense
                  style="max-height: 120px"
                  class="overflow-y-auto"
                >
                  <div v-for="(image) in data.images" :key="image.id">
                    <v-list-item class="pl-0">
                      <v-alert
                        color="success"
                        class="white--text text-center pa-1 ma-0"
                        width="100%"
                        v-text="imageName(image)"
                      />
                      <v-list-item-action>
                        <v-btn icon x-small @click="onPoiImageDeleteClick(image.id)">
                          <v-icon color="error darken-1">mdi-delete</v-icon>
                        </v-btn>
                      </v-list-item-action>
                    </v-list-item>
                  </div>
                </v-list>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
      </v-card-text>
      <v-divider class="mt-5" />
      <v-card-actions>
        <v-btn color="blue darken-1" text @click="onCloseClick">
          Cancel
        </v-btn>
        <v-btn
          :disabled="!valid"
          color="blue darken-1"
          text
          @click="onSaveClick"
        >
          <v-icon left>mdi-content-save</v-icon>
          Save
        </v-btn>
        <v-spacer />
        <v-btn
          color="error darken-1"
          text
          @click="onDeletePoiClick"
        >
          <v-icon left>mdi-delete</v-icon>
          Delete
        </v-btn>
      </v-card-actions>
    </v-card>
    <confirm-dialog
      :show="showConfirmPoiImageDelete"
      :busy="isLoading"
      @cancelClick="showConfirmPoiImageDelete = false"
      @confirmClick="deletePoiImage"
    />
    <confirm-dialog
      :show="showConfirmPoiDelete"
      :busy="isLoading"
      @cancelClick="showConfirmPoiDelete = false"
      @confirmClick="deletePoi"
    />
  </v-dialog>
</template>

<script>
import ConfirmDialog from '@/components/ConfirmDialog';

export default {
  name: 'AttributesOverlay',
  components: {
    ConfirmDialog
  },
  data () {
    return {
      isVisible: false,
      dialogWidth: 354,
      valid: true,
      requiredRule: [
        v => (v && v.trim().length > 0) || 'This field is required.'
      ],
      imageUploadRules: [
        (value) => {
          if (!value) {
            return true;
          }
          // Handle array of files for multiple selection
          if (Array.isArray(value)) {
            return value.every(file => file.size < (20 * 1024000)) || 'Each image size should be less than 20 MB!';
          }
          // Handle single file
          return value.size < (20 * 1024000) || 'Image size should be less than 20 MB!';
        }
      ],
      isLoading: false,
      showConfirmPoiDelete: false,
      showConfirmPoiImageDelete: false,
      selectedPoiImageId: null,
      data: {
        name: '',
        name_en: '',
        name_de: '',
        html_content: '',
        enabled: true,
        images: []
      },
      imageFile: null,
      imageFiles: [],
      pendingImages: [],
      pendingUpload: false, // New flag to control upload timing
      feature: null,
      isNewlyCreated: false // Track if POI was just created
    }
  },
  computed: {
    popupSize () {
      return {
        width: '354px',
        height: this.feature ? '395px' : '326px'
      };
    }
  },
  watch: {
    imageFile (newVal) {
      if (newVal) {
        this.onImageUpload();
      }
    }
  },
  methods: {
    show () {
      this.isVisible = true;
      this.$nextTick(() => {
        if (this.$refs.form) {
          this.$refs.form.resetValidation();
        }
      });
    },
    hide () {
      this.isVisible = false;
    },
    onCloseClick () {
      this.isVisible = false;
      // this.$emit('closeClick');
    },
    onSaveClick () {
      this.isNewlyCreated = !this.feature;
      this.pendingUpload = true; // Only allow uploads after save
      this.$emit('saveClick', {
        data: this.data,
        feature: this.feature,
        imageFiles: this.imageFiles
      });
      this.imageFiles = [];
    },
    // In AttributesOverlay.vue, add this method back but modify it to only collect files
    onImageUpload () {
      // Only collect files, don't trigger uploads
      if (!this.imageFile) {
        return;
      }

      // Store files for batch upload on save
      if (Array.isArray(this.imageFile)) {
        this.imageFiles.push(...this.imageFile);
      } else {
        this.imageFiles.push(this.imageFile);
      }
      this.imageFile = null;
    },
    removeSelectedImage (index) {
      this.imageFiles.splice(index, 1);
    },
    deletePoi () {
      this.isLoading = true;
      this.$emit('deleteClick', {
        data: this.data,
        feature: this.feature
      })
      this.showConfirmPoiDelete = false;
    },
    onDeletePoiClick () {
      this.showConfirmPoiDelete = true;
    },
    deletePoiImage () {
      this.isLoading = true;
      this.$emit('poiImageDeleteClick', {
        id: this.selectedPoiImageId,
        feature: this.feature
      })
    },
    onPoiImageDeleteClick (imageId) {
      this.showConfirmPoiImageDelete = true;
      this.selectedPoiImageId = imageId;
    },
    setData (data, feature) {
      this.data = { ...data };
      this.feature = feature || null;
      this.imageFile = null;
      this.isLoading = false; // Reset loading state
      this.imageFiles = []; // Reset pending uploads
      this.isNewlyCreated = false; // reset flag
      this.pendingUpload = false; // Reset upload flag
      // Reset file input
      if (this.$refs.uploadImage) {
        this.$refs.uploadImage.reset();
      }
      // Reset validation
      if (this.$refs.form) {
        this.$refs.form.resetValidation();
      }
    },
    setImages (images) {
      this.data.images = images || [];
      this.imageFile = null;
      this.$refs.uploadImage.reset();
      this.isLoading = false;
      this.selectedPoiImageId = null;
      this.showConfirmPoiImageDelete = false;
    },
    imageName (image) {
      if (image.image) {
        return image.image.split('/').pop()
      }
      return image.alt_text
    },
    selectFile () {
      const fileInput = this.$refs.uploadImage.$el.querySelector('input[type="file"]')
      const clickEvent = new MouseEvent('click')
      fileInput.dispatchEvent(clickEvent)
    }
  }
};
</script>

<style>

</style>
