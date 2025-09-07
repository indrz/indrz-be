<template>
  <div>
    <v-card>
      <v-data-table
        v-model="selected"
        :headers="headers"
        :items="shelfListData"
        :server-items-length="total"
        :single-select="singleSelect"
        :loading="loading"
        :height="height"
        :no-data-text="noDataText"
        @click:row="onIndrzEventsClick"
        item-key="id"
        dense
        class="elevation-1"
        loading-text="Loading... Please wait"
        hide-default-footer
      >
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>Shelf Data</v-toolbar-title>
            <v-spacer />
            <v-btn
              :disabled="!selectedShelf || shelfDataAddEditDialog"
              @click="addIndrzEvents"
              outlined
            >
              <v-icon left>
                mdi-plus
              </v-icon>
              Shelf Data
            </v-btn>
          </v-toolbar>
        </template>
        <template v-slot:item.building_floor="{item}">
          {{ getFloorName(item.building_floor) }}
        </template>
        <template v-slot:item.actions="{ item }">
          <v-icon
            @click="editIndrzEvents(item)"
            small
            class="mr-1"
          >
            mdi-pencil
          </v-icon>
          <v-icon
            @click="showConfirmDeleteIndrzEvents = true"
            small
          >
            mdi-delete
          </v-icon>
        </template>
      </v-data-table>
      <add-edit-shelf-data
        :title="shelfDataFormTitle"
        :dialog="shelfDataAddEditDialog"
        :current-shelf-data="shelfDataEditedItem"
        @close="shelfDataAddEditDialogClose"
      />
      <confirm-dialog
        :show="showConfirmDeleteIndrzEvents"
        :message="deleteIndrzEventsConfirmMessage"
        :busy="loading"
        @cancelClick="showConfirmDeleteIndrzEvents = false"
        @confirmClick="confirmDeleteIndrzEvents"
      />
    </v-card>
  </div>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex';
import ConfirmDialog from '@/components/ConfirmDialog';
import AddEditIndrzEvents from '@/components/admin/events/AddEditIndrzEvents';

export default {
  name: 'IndrzEventsList',
  components: { ConfirmDialog, AddEditIndrzEvents },
  props: {
    height: {
      type: Number,
      default: 285
    }
  },
  data () {
    return {
      loading: false,
      singleSelect: false,
      shelfDataAddEditDialog: false,
      showConfirmDeleteIndrzEvents: false,
      selected: [],
      headers: [
        {
          text: 'External Id',
          align: 'left',
          sortable: false,
          value: 'external_id',
          width: 90
        },
        {
          text: 'Floor',
          align: 'right',
          filterable: false,
          sortable: false,
          value: 'building_floor'
        },
        {
          text: 'System From',
          align: 'right',
          sortable: true,
          value: 'system_from'
        },
        {
          text: 'System To',
          align: 'right',
          sortable: true,
          value: 'system_to'
        },
        {
          text: 'Shelf Side',
          align: 'right',
          filterable: false,
          sortable: false,
          value: 'side'
        },
        {
          text: 'Measure From',
          align: 'right',
          filterable: false,
          sortable: false,
          value: 'measure_from'
        },
        {
          text: 'Measure To',
          align: 'right',
          filterable: false,
          sortable: false,
          value: 'measure_to'
        },
        { text: '', value: 'actions', sortable: false }
      ],
      shelfDataEditedIndex: -1,
      shelfDataEditedItem: {},
      defaultItem: {
        bookshelf_id: null,
        external_id: null,
        floor: null,
        id: null,
        measure_from: null,
        measure_to: null,
        section_child: null,
        section_id: null,
        section_main: null,
        side: 'L',
        system_from: null,
        system_to: null
      },
      deleteIndrzEventsConfirmMessage: 'Are you sure to delete this shelf data?'
    };
  },
  computed: {
    ...mapState({
      shelfListData: function (state) {
        const { data, total } = state.shelf.shelfData;

        this.total = total;

        return data;
      },
      noDataText: (state) => {
        if (state.shelf.selectedShelf) {
          return 'No shelf data found';
        }
        return 'No book shelf selected';
      },
      floors: state => state.floor.floors,
      buildings: state => state.building.buildings,
      selectedShelf: state => state.shelf.selectedShelf,
      selectedIndrzEvents: state => state.shelf.selectedIndrzEvents
    }),
    ...mapGetters({
      getFloorName: 'building/getFloorName',
      firstBuilding: 'building/firstBuilding',
      firstFloor: 'building/firstFloor'

    }),
    shelfDataFormTitle () {
      return this.shelfDataEditedIndex === -1 ? 'New Shelf Data' : 'Edit Shelf Data';
    }
  },
  watch: {
    shelfDataAddEditDialog (val) {
      val || this.shelfDataAddEditDialogClose();
    }
  },
  methods: {
    ...mapActions({
      loadShelfList: 'shelf/LOAD_BOOKSHELF_LIST',
      loadFloors: 'building/LOAD_FLOORS',
      deleteIndrzEvents: 'shelf/DELETE_SHELF_DATA',
      setSelectedIndrzEvents: 'shelf/SET_SELECTED_SHELF_DATA'
    }),
    onIndrzEventsClick (data) {
      this.setSelectedIndrzEvents(data);
    },

    async addIndrzEvents () {
      await this.loadFloors();

      this.shelfDataEditedItem = Object.assign({
        building: this.firstBuilding(),
        building_floor: this.firstFloor(),
        bookshelf: this.selectedShelf.id
      });

      this.shelfDataAddEditDialog = true;
    },

    async editIndrzEvents (shelfData) {
      await this.loadFloors(shelfData.building);

      this.shelfDataEditedIndex = this.shelfListData.indexOf(shelfData);
      this.shelfDataEditedItem = Object.assign({}, shelfData);
      this.shelfDataAddEditDialog = true;
    },

    async confirmDeleteIndrzEvents () {
      this.loading = true;

      await this.deleteIndrzEvents(this.selectedIndrzEvents);

      this.showConfirmDeleteIndrzEvents = false;
      this.loading = false;
    },

    shelfDataAddEditDialogClose () {
      this.shelfDataAddEditDialog = false;
      /* setTimeout(() => {
        this.shelfDataEditedItem = Object.assign({}, this.defaultItem);
        this.shelfDataEditedIndex = -1;
      }, 300); */
    }
  }
};
</script>

<style scoped>

</style>
