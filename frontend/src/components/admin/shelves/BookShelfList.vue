<template>
  <v-card>
    <v-data-table
      :headers="headers"
      :items="shelvesListData"
      :items-length="total"
      v-model:options="pagination"
      :loading="loading"
      :height="height"
      :items-per-page-options="[25, 50, 100]"
      @click:row="onShelfClick"
      density="compact"
      item-value="id"
      class="elevation-1"
      loading-text="Loading... Please wait"
    >
      <template v-slot:top>
        <v-toolbar elevation="0">
          <v-toolbar-title>Book Shelves</v-toolbar-title>
          <v-spacer />
          <v-text-field
            v-model="search"
            label="Search"
            clearable
            single-line
            hide-details
          />
          <v-divider
            class="mx-4"
            inset
            vertical
          />
          <v-btn
            :disabled="bookShelfAddEditDialog"
            @click="addBookShelf"
            variant="outlined"
          >
            <v-icon start>
              mdi-plus
            </v-icon>
            Book Shelf
          </v-btn>
        </v-toolbar>
      </template>
      <template v-slot:[`item.building`]="{ item }">
        {{ getBuildingName(item.building) }}
      </template>
      <template v-slot:[`item.actions`]="{ item }">
        <v-icon
          @click.stop="onBookShelfDrawClick(item)"
          class="mr-1"
          size="small"
        >
          mdi-map
        </v-icon>
        <v-icon
          @click.stop="editBookShelf(item)"
          class="mr-1"
          size="small"
        >
          mdi-pencil
        </v-icon>
        <v-icon
          @click.stop="deleteShelfItem(item)"
          size="small"
        >
          mdi-delete
        </v-icon>
      </template>
    </v-data-table>
    <add-edit-shelf
      :title="bookShelfFormTitle"
      :dialog="bookShelfAddEditDialog"
      :current-shelf="bookShelfEditedItem"
      @close="bookShelfAddEditDialogClose"
    />
    <draw-shelf
      :title="drawShelfTitle"
      :show="bookShelfDrawDialog"
      @save="saveBookShelfGeometry"
      @close="bookShelfDrawDialogClose"
    />
    <confirm-dialog
      :show="showConfirmDeleteShelf"
      :message="deleteShelfConfirmMessage"
      :busy="loading"
      @cancelClick="showConfirmDeleteShelf = false"
      @confirmClick="confirmDeleteBookShelf"
    />
  </v-card>
</template>

<script>
import { Subject } from 'rxjs';
import { debounceTime, distinctUntilChanged, filter } from 'rxjs/operators';
import AddEditShelf from '@/components/admin/shelves/AddEditShelf';
import DrawShelf from '@/components/admin/shelves/DrawShelf';
import ConfirmDialog from '@/components/ConfirmDialog';
import api from '@/util/api';
import { getGeomFromCoordinates } from '@/util/misc';
import { useShelfStore } from '~/stores/shelf';
import { useFloorStore } from '~/stores/floor';
import { useBuildingStore } from '~/stores/building';

export default {
  name: 'BookShelfList',
  components: { DrawShelf, ConfirmDialog, AddEditShelf },
  props: {
    height: {
      type: Number,
      default: 600
    }
  },
  data () {
    return {
      loading: false,
      singleSelect: false,
      bookShelfAddEditDialog: false,
      bookShelfDrawDialog: false,
      showConfirmDeleteShelf: false,
      selected: [],
      pagination: {},
      search: '',
      term$: new Subject(),
      headers: [
        {
          title: 'Id',
          align: 'right',
          sortable: false,
          key: 'id'
        },
        {
          title: 'External Id',
          align: 'left',
          sortable: false,
          key: 'external_id',
          width: 90
        },
        {
          title: 'Building',
          align: 'left',
          filterable: false,
          sortable: false,
          key: 'building',
          width: 150
        },
        {
          title: 'Floor',
          align: 'left',
          filterable: false,
          sortable: false,
          key: 'floor_name',
          width: 100
        },
        {
          title: 'Length',
          align: 'right',
          filterable: false,
          sortable: false,
          key: 'length'
        },
        {
          title: 'Width',
          align: 'right',
          filterable: false,
          sortable: false,
          key: 'width'
        },
        {
          title: 'Left From Label',
          align: 'left',
          sortable: true,
          key: 'left_from_label'
        },
        {
          title: 'Left To Label',
          align: 'left',
          sortable: true,
          key: 'left_to_label'
        },
        {
          title: 'Right From Label',
          align: 'left',
          sortable: true,
          key: 'right_from_label'
        },
        {
          title: 'Right To Label',
          align: 'left',
          sortable: true,
          key: 'right_to_label'
        },
        { title: '', key: 'actions', width: 120, sortable: false }
      ],
      bookShelfEditedIndex: -1,
      bookShelfEditedItem: {},
      shelfToDelete: null,
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
      deleteShelfConfirmMessage: 'All shelf data will be deleted. DO YOU REALLY WANT TO DELETE THE BOOKSHELF?'
    };
  },
  computed: {
    shelvesListData () {
      const shelfStore = useShelfStore();
      const { data = [], total = 0 } = shelfStore.shelves || {};
      const tableData = [];

      this.total = total;

      data.forEach((d) => {
        tableData.push({ ...d.properties, id: d.id, geometry: d.geometry });
      });
      return tableData;
    },
    total () {
      const shelfStore = useShelfStore();
      const { total = 0 } = shelfStore.shelves || {};
      return total;
    },
    selectedShelf () {
      const shelfStore = useShelfStore();
      return shelfStore.selectedShelf;
    },
    floors () {
      const floorStore = useFloorStore();
      return typeof floorStore.floors === 'function' ? floorStore.floors() : floorStore.$state.floors;
    },
    buildings () {
      const buildingStore = useBuildingStore();
      return buildingStore.buildings;
    },
    getBuildingName () {
      const buildingStore = useBuildingStore();
      return buildingStore.getBuildingName;
    },
    firstBuilding () {
      const buildingStore = useBuildingStore();
      return buildingStore.firstBuilding;
    },
    firstFloor () {
      const floorStore = useFloorStore();
      return floorStore.firstFloor;
    },
    getFloorName () {
      const floorStore = useFloorStore();
      return floorStore.getFloorName;
    },
    bookShelfFormTitle () {
      return this.bookShelfEditedIndex === -1 ? 'New Shelf' : 'Edit Shelf';
    },
    drawShelfTitle () {
      return 'Draw Shelf';
    }
  },
  watch: {
    search (text) {
      this.term$.next(text);
    },
    bookShelfAddEditDialog (val) {
      val || this.bookShelfAddEditDialogClose();
    },
    bookShelfDrawDialog (val) {
      val || this.bookShelfDrawDialogClose();
    },
    pagination: {
      handler () {
        this.loadData();
      },
      deep: true
    }
  },
  mounted () {
    this
      .term$
      .pipe(
        filter(term => !term || term.length > 2),
        debounceTime(500),
        distinctUntilChanged()
      )
      .subscribe(term => this.loadData(term));
    this.loadFloors();
    this.loadData();
  },
  methods: {
    loadShelfList (query) {
      const shelfStore = useShelfStore();
      return shelfStore.LOAD_BOOKSHELF_LIST(query);
    },
    loadFloors () {
        const floorStore = useFloorStore();
        return floorStore.LOAD_FLOORS();
    },
    deleteBookShelf (shelf) {
      const shelfStore = useShelfStore();
      return shelfStore.DELETE_SHELF(shelf);
    },
    saveShelf (payload) {
      const shelfStore = useShelfStore();
      return shelfStore.SAVE_SHELF(payload);
    },
    setSelectedShelf (shelf) {
      const shelfStore = useShelfStore();
      return shelfStore.SET_SELECTED_SHELF(shelf);
    },
    onShelfClick (event, row) {
      this.setSelectedShelf(row?.item ?? event);
    },
    deleteShelfItem (shelf) {
      this.shelfToDelete = shelf;
      this.showConfirmDeleteShelf = true;
    },
    async loadData (term) {
      if (this.loading) {
        return;
      }

      this.loading = true;
      const query = api.getPageParams(this.pagination);

      if (term) {
        query.search = term;
      }

      await this.loadShelfList(query);

      this.loading = false;
    },

    addBookShelf () {
      this.setSelectedShelf(null);

      this.bookShelfEditedItem = Object.assign({
        double_sided: true,
        building: this.firstBuilding(),
        building_floor: this.firstFloor()
      });
      this.bookShelfAddEditDialog = true;
    },

    onBookShelfDrawClick (shelf) {
      this.setSelectedShelf(shelf);
      this.bookShelfDrawDialog = true;
    },

    editBookShelf (bookShelf) {
      this.bookShelfEditedIndex = this.shelvesListData.indexOf(bookShelf);

      this.bookShelfEditedItem = Object.assign({}, bookShelf);
      const { geometry } = this.bookShelfEditedItem;
      if (geometry && geometry?.coordinates?.length) {
        this.bookShelfEditedItem.geom = getGeomFromCoordinates(geometry.coordinates[0]);
      }
      this.bookShelfAddEditDialog = true;
    },

    async confirmDeleteBookShelf () {
      this.loading = true;

      await this.deleteBookShelf(this.shelfToDelete);

      this.shelfToDelete = null;
      this.showConfirmDeleteShelf = false;
      this.loading = false;
    },

    bookShelfAddEditDialogClose () {
      this.bookShelfAddEditDialog = false;
      setTimeout(() => {
        this.bookShelfEditedItem = Object.assign({}, this.defaultItem);
        this.bookShelfEditedIndex = -1;
      }, 300);
    },
    bookShelfDrawDialogClose () {
      this.bookShelfDrawDialog = false;
    },
    async saveBookShelfGeometry ({ coordinates, floor }) {
      this.loading = true;

      const currentShelf = { ...this.selectedShelf };

      currentShelf.geometry && delete currentShelf.geometry;
      if (floor) {
        currentShelf.building_floor = floor.id;
      }

      currentShelf.geom = getGeomFromCoordinates(coordinates);

      await this.saveShelf(currentShelf);

      this.loading = false;
    }
  }
};
</script>

<style scoped>

</style>
