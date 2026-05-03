<template>
  <div>
    <v-card>
      <v-data-table
        :headers="headers"
        :items="shelfListData"
        :loading="loading"
        :height="height"
        :no-data-text="noDataText"
        @click:row="onIndrzEventsClick"
        density="compact"
        class="elevation-1"
        loading-text="Loading... Please wait"
        hide-default-footer
      >
        <template v-slot:top>
          <v-toolbar elevation="0">
            <v-toolbar-title>Shelf Data</v-toolbar-title>
            <v-spacer />
            <v-btn
              :disabled="!selectedShelf || shelfDataAddEditDialog"
              @click="addIndrzEvents"
              variant="outlined"
            >
              <v-icon start>
                mdi-plus
              </v-icon>
              Shelf Data
            </v-btn>
          </v-toolbar>
        </template>
        <template v-slot:item.building_floor="{ item }">
          {{ getFloorName(item.raw.building_floor) }}
        </template>
        <template v-slot:item.actions="{ item }">
          <v-icon
            @click="editIndrzEvents(item.raw)"
            size="small"
            class="mr-1"
          >
            mdi-pencil
          </v-icon>
          <v-icon
            @click="showConfirmDeleteIndrzEvents = true"
            size="small"
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
import ConfirmDialog from '@/components/ConfirmDialog';
import AddEditIndrzEvents from '@/components/admin/events/AddEditIndrzEvents';
import { useShelfStore } from '~/stores/shelf';
import { useFloorStore } from '~/stores/floor';
import { useBuildingStore } from '~/stores/building';

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
          title: 'External Id',
          align: 'left',
          sortable: false,
          key: 'external_id',
          width: 90
        },
        {
          title: 'Floor',
          align: 'right',
          filterable: false,
          sortable: false,
          key: 'building_floor'
        },
        {
          title: 'System From',
          align: 'right',
          sortable: true,
          key: 'system_from'
        },
        {
          title: 'System To',
          align: 'right',
          sortable: true,
          key: 'system_to'
        },
        {
          title: 'Shelf Side',
          align: 'right',
          filterable: false,
          sortable: false,
          key: 'side'
        },
        {
          title: 'Measure From',
          align: 'right',
          filterable: false,
          sortable: false,
          key: 'measure_from'
        },
        {
          title: 'Measure To',
          align: 'right',
          filterable: false,
          sortable: false,
          key: 'measure_to'
        },
        { title: '', key: 'actions', sortable: false }
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
    shelfListData () {
      const shelfStore = useShelfStore();
      const { data = [], total = 0 } = shelfStore.shelfData || {};

      this.total = total;

      return data;
    },
    noDataText () {
      const shelfStore = useShelfStore();
      if (shelfStore.selectedShelf) {
        return 'No shelf data found';
      }
      return 'No book shelf selected';
    },
    floors () {
      const floorStore = useFloorStore();
      return typeof floorStore.floors === 'function' ? floorStore.floors() : floorStore.$state.floors;
    },
    buildings () {
      const buildingStore = useBuildingStore();
      return buildingStore.buildings;
    },
    selectedShelf () {
      const shelfStore = useShelfStore();
      return shelfStore.selectedShelf;
    },
    selectedIndrzEvents () {
      const shelfStore = useShelfStore();
      return shelfStore.selectedShelfData;
    },
    getFloorName () {
      const buildingStore = useBuildingStore();
      return buildingStore.getFloorName;
    },
    firstBuilding () {
      const buildingStore = useBuildingStore();
      return buildingStore.firstBuilding;
    },
    firstFloor () {
      const buildingStore = useBuildingStore();
      return buildingStore.firstFloor;
    },
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
    loadShelfList (query) {
      const shelfStore = useShelfStore();
      return shelfStore.LOAD_BOOKSHELF_LIST(query);
    },
    loadFloors (buildingId) {
      const buildingStore = useBuildingStore();
      return buildingStore.LOAD_FLOORS(buildingId);
    },
    deleteIndrzEvents (payload) {
      const shelfStore = useShelfStore();
      return shelfStore.DELETE_SHELF_DATA(payload);
    },
    setSelectedIndrzEvents (payload) {
      const shelfStore = useShelfStore();
      return shelfStore.SET_SELECTED_SHELF_DATA(payload);
    },
    onIndrzEventsClick (event, row) {
      const indrzEvent = row?.item?.raw || row?.item || row?.raw || event?.item?.raw || event;
      this.setSelectedIndrzEvents(indrzEvent);
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
