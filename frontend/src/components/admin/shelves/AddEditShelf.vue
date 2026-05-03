<template>
  <v-dialog :model-value="dialog" persistent scrollable max-width="500px">
    <v-card>
      <v-toolbar
        density="compact"
        elevation="0"
      >
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
                <v-text-field v-model="localShelf.external_id" :rules="requiredRule" label="External Id" />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-text-field
                  v-model="localShelf.geom"
                  @click:append-inner="onGeomButtonClick"
                  label="Geometry"
                  clear-icon="mdi-close-circle"
                  append-inner-icon="mdi-map"
                  clearable
                />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-text-field v-model="localShelf.left_from_label" :rules="requiredRule" label="Left From Label" />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-text-field v-model="localShelf.left_to_label" :rules="requiredRule" label="Left To Label" />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-text-field v-model="localShelf.right_from_label" :rules="requiredRule" label="Right From Label" />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-text-field v-model="localShelf.right_to_label" :rules="requiredRule" label="Right To Label" />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-select
                  v-model="localShelf.building"
                  :items="buildings"
                  :rules="requiredRule"
                  item-title="properties.building_name"
                  item-value="id"
                  label="Building"
                />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-select
                  v-model="localShelf.building_floor"
                  :items="floors"
                  :rules="requiredRule"
                  item-title="floor_name"
                  item-value="id"
                  label="Building Floor"
                />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-text-field v-model="localShelf.measure_from" :rules="requiredRule" label="Measure From" />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-text-field v-model="localShelf.measure_to" :rules="requiredRule" label="Measure To" />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-text-field v-model="localShelf.length" type="number" min="0" step="0.01" label="Length in m" />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-text-field v-model="localShelf.width" type="number" min="0" step="0.01" label="Width in m" />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-text-field v-model="localShelf.depth" type="number" min="0" step="0.01" label="Depth in m" />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-text-field v-model="localShelf.rotation" type="number" step="1" label="Rotation angle" />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-select
                  v-model="localShelf.double_sided"
                  :items="doubleSidedItems"
                  item-title="text"
                  item-value="value"
                  label="Does the shelf have two sides"
                />
              </v-col>
            </v-row>
          </v-container>
        </v-form>
      </v-card-text>
      <v-divider />
      <v-card-actions>
        <v-spacer />
        <v-btn :disabled="loading" @click="close" color="blue-darken-1" variant="text">
          Cancel
        </v-btn>
        <v-btn
          :disabled="loading || !valid"
          :loading="loading"
          @click="save"
          color="blue-darken-1"
          variant="text"
        >
          <v-icon start>
            mdi-content-save
          </v-icon>
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
    <draw-shelf
      :title="drawShelfTitle"
      :show="bookShelfDrawDialog"
      @save="setGeometry"
      @close="bookShelfDrawDialogClose"
    />
  </v-dialog>
</template>

<script>
import { getGeomFromCoordinates } from '@/util/misc';
import DrawShelf from '@/components/admin/shelves/DrawShelf';
import { useFloorStore } from '~/stores/floor';
import { useBuildingStore } from '~/stores/building';
import { useShelfStore } from '~/stores/shelf';

export default {
  name: 'AddEditShelf',
  components: { DrawShelf },
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
    currentShelf: {
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
      bookShelfDrawDialog: false,
      doubleSidedItems: [
        { text: 'Unknown', value: null },
        { text: 'Yes', value: true },
        { text: 'No', value: false }
      ],
      requiredRule: [
        v => !!v || 'This field is required.'
      ],
      localShelf: {
        ...this.currentShelf,
        building_floor: this.currentShelf && this.currentShelf.building_floor != null
          ? Number(this.currentShelf.building_floor)
          : null
      }
    };
  },
  computed: {
    floors () {
      const floorStore = useFloorStore();
      return typeof floorStore.floors === 'function' ? floorStore.floors() : floorStore.$state.floors;
    },
    buildings () {
      const buildingStore = useBuildingStore();
      return buildingStore.buildings;
    },
    drawShelfTitle () {
      return 'Draw Shelf';
    }
  },
  watch: {
    currentShelf (val) {
      this.localShelf = {
        ...val,
        building_floor: val && val.building_floor != null ? Number(val.building_floor) : null
      };
      if (this.$refs.form) {
        this.$refs.form.resetValidation();
      }
    },
    bookShelfDrawDialog (val) {
      val || this.bookShelfDrawDialogClose();
    }
  },
  methods: {
    saveShelf (payload) {
      const shelfStore = useShelfStore();
      return shelfStore.SAVE_SHELF(payload);
    },
    onGeomButtonClick () {
      this.bookShelfDrawDialog = true;
    },
    close () {
      this.$refs.form.reset();
      this.$refs.form.resetValidation();
      this.$emit('close');
    },
    setGeometry ({ coordinates, floor }) {
      this.localShelf.geom = getGeomFromCoordinates(coordinates);
      if (floor) {
        this.localShelf.building_floor = floor.id;
      }
    },
    bookShelfDrawDialogClose () {
      this.bookShelfDrawDialog = false;
    },
    async save () {
      const isValid = await this.$refs.form.validate();
      if (!isValid) {
        return;
      }
      this.loading = true;

      await this.saveShelf(this.localShelf);

      this.loading = false;
      this.$emit('update:currentShelf', this.localShelf);
      this.close();
    }
  }
};
</script>

<style scoped>

</style>
