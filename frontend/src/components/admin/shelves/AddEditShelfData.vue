The error `Unexpected mutation of "currentShelfData" prop vue/no-mutating-props` occurs because you are directly modifying the `currentShelfData` prop, which is not recommended in Vue.js. Instead, you should use a local copy of the prop and modify that.

Here is how you can fix it:

1. Create a local copy of the `currentShelfData` prop in the `data` function.
2. Use the local copy in your template and methods.
3. Emit an event to update the parent component when changes are made.

```vue
<template>
  <v-card-text>
    <v-form
      ref="form"
      v-model="valid"
      lazy-validation
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
              item-text="text"
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
</template>

<script>
import { mapActions } from 'vuex';

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
    dialog: function (newValue) {
      if (newValue === true && !this.currentShelfData.id && this.$refs?.form) {
        this.$refs.form.resetValidation();
      }
    }
  },
  methods: {
    ...mapActions({
      saveShelfData: 'shelf/SAVE_SHELF_DATA'
    }),
    close () {
      this.$refs.form.reset();
      this.$refs.form.resetValidation();
      this.$emit('close');
    },
    async save () {
      if (!this.$refs.form.validate()) {
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
```
