<template>
  <v-dialog :model-value="dialog" persistent scrollable max-width="500px">
    <v-card>
      <v-toolbar density="compact" elevation="0">
        <div class="text-h6">
          {{ title }}
        </div>
        <v-spacer />
        <v-btn @click="close" icon>
          <v-icon>mdi-window-close</v-icon>
        </v-btn>
      </v-toolbar>
      <v-card-text>
        <v-form
          ref="form"
          v-model="valid"
        >
          <v-container>
            <v-row no-gutters>
              <v-col>
                <v-text-field v-model="localShelfData.external_id" :rules="requiredRule" label="External Id" />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-text-field v-model="localShelfData.section_main" label="Main Section" />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-text-field v-model="localShelfData.section_child" label="Sub Section" />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-text-field
                  v-model="localShelfData.system_from"
                  :rules="requiredRule"
                  label="Shelving System Start"
                />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-text-field
                  v-model="localShelfData.system_to"
                  :rules="requiredRule"
                  label="Shelving System End"
                />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-select
                  v-model="localShelfData.side"
                  :items="leftOrRightItems"
                  item-title="text"
                  item-value="value"
                  label="Side"
                />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-text-field
                  v-model="localShelfData.measure_from"
                  type="number"
                  min="0"
                  step="0.01"
                  label="Distance from measure"
                />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-text-field
                  v-model="localShelfData.measure_to"
                  type="number"
                  min="0"
                  step="0.01"
                  label="Distance to measure"
                />
              </v-col>
            </v-row>
          </v-container>
        </v-form>
      </v-card-text>
      <v-divider />
      <v-card-actions>
        <v-spacer />
        <v-btn :disabled="loading" @click="close" variant="text">
          Cancel
        </v-btn>
        <v-btn
          :disabled="loading || !valid"
          :loading="loading"
          @click="save"
          variant="text"
          prepend-icon="mdi-content-save"
        >
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { useShelfStore } from '~/stores/shelf';

export default {
  name: 'AddEditShelfData',
  props: {
    title: {
      type: String,
      default: function () {
        return '';
      }
    },
    dialog: {
      type: Boolean,
      default: function () {
        return false;
      }
    },
    currentShelfData: {
      type: Object,
      default: function () {
        return {};
      }
    }
  },
  data () {
    return {
      loading: false,
      valid: true,
      leftOrRightItems: [
        { text: 'Unknown', value: null },
        { text: 'Left', value: 'L' },
        { text: 'Right', value: 'R' }
      ],
      requiredRule: [
        v => !!v || 'This field is required.'
      ],
      localShelfData: { ...this.currentShelfData }
    };
  },
  watch: {
    currentShelfData: {
      handler (newValue) {
        this.localShelfData = { ...newValue };
      },
      deep: true
    },
    dialog: function (newValue) {
      if (newValue === true && !this.currentShelfData.id && this.$refs?.form) {
        this.$refs.form.resetValidation();
      }
    }
  },
  methods: {
    async saveShelfData (payload) {
      const shelfStore = useShelfStore();
      await shelfStore.SAVE_SHELF_DATA(payload);
    },
    close () {
      this.$refs.form.reset();
      this.$refs.form.resetValidation();
      this.$emit('close');
    },
    async save () {
      const { valid } = await this.$refs.form.validate();
      if (!valid) {
        return;
      }
      this.loading = true;

      await this.saveShelfData(this.localShelfData);

      this.loading = false;
      this.$emit('update:currentShelfData', this.localShelfData);
      this.close();
    }
  }
};
</script>

<style scoped>

</style>
