<template>
  <v-dialog :value="dialog" persistent scrollable max-width="500px">
    <v-card>
      <v-toolbar
        dense
        flat
      >
        <div class="headline">
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
          lazy-validation
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
                  @click:append-outer="onGeomButtonClick"
                  label="Geometry"
                  clear-icon="mdi-close-circle"
                  append-outer-icon="mdi-map"
                  clearable
                />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-text-field v-model="localShelf.left_from_label" label="Left From Label" />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-text-field v-model="localShelf.left_to_label" label="Left To Label" />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-text-field v-model="localShelf.right_from_label" label="Right From Label" />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-text-field v-model="localShelf.right_to_label" label="Right To Label" />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-select
                  v-model="localShelf.building"
                  :items="buildings"
                  item-text="building_name"
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
                  item-text="short_name"
                  item-value="id"
                  label="Building Floor"
                />
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
                  item-text="text"
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
        <v-btn :disabled="loading" @click="close" color="blue darken-1" text>
          Cancel
        </v-btn>
        <v-btn
          :disabled="loading || !valid"
          :loading="loading"
          @click="save"
          color="blue darken-1"
          text
        >
          <v-icon left>
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
import { mapState, mapActions } from 'vuex';
import { getGeomFromCoordinates } from '@/util/misc';
import DrawShelf from '@/components/admin/shelves/DrawShelf';

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
      localShelf: { ...this.currentShelf }
    };
  },
  computed: {
    ...mapState({
      floors: state => state.floor.floors,
      buildings: state => state.building.buildings
    }),
    drawShelfTitle () {
      return 'Draw Shelf';
    }
  },
  watch: {
    bookShelfDrawDialog (val) {
      val || this.bookShelfDrawDialogClose();
    }
  },
  methods: {
    ...mapActions({
      saveShelf: 'shelf/SAVE_SHELF'
    }),
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
      if (!this.$refs.form.validate()) {
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
