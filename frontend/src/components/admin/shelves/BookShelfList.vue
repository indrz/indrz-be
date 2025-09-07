<template>
  <v-card>
    <v-data-table
      v-model="selected"
      :headers="headers"
      :items="shelvesListData"
      :server-items-length="total"
      :single-select="singleSelect"
      :options.sync="pagination"
      :loading="loading"
      :height="height"
      :footer-props="{
        'items-per-page-options': [25, 50, 100]
      }"
      @click:row="onShelfClick"
      dense
      item-key="id"
      class="elevation-1"
      loading-text="Loading... Please wait"
    >
      <template v-slot:top>
        <v-toolbar flat>
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
            outlined
          >
            <v-icon left>
              mdi-plus
            </v-icon>
            Book Shelf
          </v-btn>
        </v-toolbar>
      </template>
      <template v-slot:[`item.building`]="{item}">
        {{ getBuildingName(item.building) }}
      </template>
      <template v-slot:[`item.building_floor`]="{item}">
        {{ getFloorName(item.building_floor) }}
      </template>
      <template v-slot:[`item.actions`]="{ item }">
        <v-icon
          @click="onBookShelfDrawClick(item)"
          class="mr-1"
          small
        >
          mdi-map
        </v-icon>
        <v-icon
          @click="editBookShelf(item)"
          class="mr-1"
          small
        >
          mdi-pencil
        </v-icon>
        <v-icon
          @click="showConfirmDeleteShelf = true"
          small
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
import { mapState, mapActions, mapGetters } from 'vuex';
import { Subject } from 'rxjs';
import { debounceTime, distinctUntilChanged, filter } from 'rxjs/operators';
import AddEditShelf from '@/components/admin/shelves/AddEditShelf';
import DrawShelf from '@/components/admin/shelves/DrawShelf';
import ConfirmDialog from '@/components/ConfirmDialog';
import api from '@/util/api';
import { getGeomFromCoordinates } from '@/util/misc';

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
          text: 'Id',
          align: 'right',
          sortable: false,
          value: 'id'
        },
        {
          text: 'External Id',
          align: 'left',
          sortable: false,
          value: 'external_id',
          width: 90
        },
        {
          text: 'Building',
          align: 'left',
          filterable: false,
          sortable: false,
          value: 'building',
          width: 150
        },
        {
          text: 'Floor',
          align: 'left',
          filterable: false,
          sortable: false,
          value: 'building_floor',
          width: 100
        },
        {
          text: 'Length',
          align: 'right',
          filterable: false,
          sortable: false,
          value: 'length'
        },
        {
          text: 'Width',
          align: 'right',
          filterable: false,
          sortable: false,
          value: 'width'
        },
        {
          text: 'Left From Label',
          align: 'left',
          sortable: true,
          value: 'left_from_label'
        },
        {
          text: 'Left To Label',
          align: 'left',
          sortable: true,
          value: 'left_to_label'
        },
        {
          text: 'Right From Label',
          align: 'left',
          sortable: true,
          value: 'right_from_label'
        },
        {
          text: 'Right To Label',
          align: 'left',
          sortable: true,
          value: 'right_to_label'
        },
        { text: '', value: 'actions', width: 120, sortable: false }
      ],
      bookShelfEditedIndex: -1,
      bookShelfEditedItem: {},
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
    ...mapState({
      shelvesListData: function (state) {
        const { data, total } = state.shelf.shelves;
        const tableData = [];

        this.total = total;

        data.forEach((d) => {
          tableData.push({ ...d.properties, id: d.id, geometry: d.geometry });
        });
        return tableData;
      },
      selectedShelf: state => state.shelf.selectedShelf,
      floors: state => state.floor.floors,
      buildings: state => state.building.buildings
    }),
    ...mapGetters({
      getBuildingName: 'building/getBuildingName',
      firstBuilding: 'building/firstBuilding',
      firstFloor: 'floor/firstFloor',
      getFloorName: 'floor/getFloorName'
    }),
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
    this.loadData();
  },
  methods: {
    ...mapActions({
      loadShelfList: 'shelf/LOAD_BOOKSHELF_LIST',
      deleteBookShelf: 'shelf/DELETE_SHELF',
      saveShelf: 'shelf/SAVE_SHELF',
      setSelectedShelf: 'shelf/SET_SELECTED_SHELF'
    }),
    onShelfClick (shelf) {
      this.setSelectedShelf(shelf);
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

      await this.deleteBookShelf(this.selectedShelf);

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
