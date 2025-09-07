<template>
  <div>
    <poi-map
      ref="map"
      :selected-poi-category="selectedPoiCategory"
      :active-floor="activeFloor"
      @floorChange="onMapFloorChange"
      @editPoi="onEditPoi"
      @updatePoiCoord="onUpdatePoiCoord"
      @saveAddPoi="saveAddPoi"
      @saveEditPoi="saveEditPoi"
      @deletePoi="deletePoi"
      @cancelChanges="cleanupAndRemoveInteraction(false)"
    />
    <div class="poi">
      <points-of-interest
        ref="poiTree"
        :multi="false"
        :initial-poi-cat-id="initialPoiCatId"
        @selectPoiCategory="setSelectedPoiCategory"
      />
    </div>
    <div class="save-btn-panel">
      <v-btn
        :disabled="!changes"
        color="primary"
        width="70px"
        small
        @click.stop.prevent="onSaveButtonClick(true)"
      >
        Save
      </v-btn>
      <v-btn
        color="primary"
        width="70px"
        small
        @click.stop.prevent="cleanupAndRemoveInteraction(false)"
      >
        Cancel
      </v-btn>
    </div>
    <floor-changer
      ref="floorChanger"
      @floorClick="onFloorClick"
    />
    <action-buttons @action="handleAction" />
    <v-dialog
      v-model="unsavedChanges"
      persistent
      max-width="350"
    >
      <v-card>
        <v-card-title class="break-word">
          There are unsaved changes. Do you want to save changes?
        </v-card-title>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="error darken-1"
            text
            @click="onSaveButtonClick(false)"
          >
            Yes
          </v-btn>
          <v-btn
            color="blue darken-1"
            text
            @click="cleanUp"
          >
            No
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import PointsOfInterest from '../../poi/PointsOfInterest';
import FloorChanger from '../../FloorChanger';
import PoiMap from './PoiMap';
import ActionButtons from './ActionButtons';
import MapUtil from '~/util/map';
import api from '~/util/api';
import 'ol/ol.css';

export default {
  name: 'PoiManager',
  components: {
    PoiMap,
    ActionButtons,
    FloorChanger,
    PointsOfInterest
  },
  data () {
    return {
      activeFloor: null,
      activeFloorNum: '',
      selectedPoiCategory: null,
      floors: [],
      newPoiCollection: [],
      editPoi: null,
      initialPoiCatId: [],
      unsavedChanges: false,
      mapComp: null,
      lastLoadedData: {}
    };
  },

  computed: {
    changes () {
      const mapComp = this.mapComp;
      return mapComp && (
        mapComp.newPois.length ||
        mapComp.removePois.length ||
        mapComp.editPois.length
      );
    }
  },

  mounted () {
    this.$root.$on('poiLoad', (data) => {
      this.lastLoadedData = { ...data };
      if (this.$refs.map) {
        this.$refs.map.onPoiLoad(data);
      }
    });
    this.$root.$on('deletePois', this.deletePois);
    this.mapComp = this.$refs.map;
  },

  methods: {
    setSelectedPoiCategory (poiCategory) {
      this.selectedPoiCategory = poiCategory;

      if (!this.selectedPoiCategory) {
        this.cleanupAndRemoveInteraction(true);
        return;
      }
      if (this.changes) {
        this.unsavedChanges = true;
      } else {
        this.$refs.map.removeInteraction(true);
      }
    },
    onFloorClick (floorNum) {
      this.activeFloorNum = floorNum;
      this.activeFloor = this.$refs.floorChanger.getFloorByFloorNum(floorNum);
      const { map, layers } = this.$refs.map;
      MapUtil.activateLayer(this.activeFloorNum, layers.switchableLayers, map);
    },
    onMapFloorChange ({ floor, floorNum }) {
      this.activeFloor = floor;
      this.$nextTick(function () {
        this.$refs.floorChanger.onFloorClick(floor);
        this.activeFloorNum = floorNum;
      });
    },
    onEditPoi (poi) {
      this.editPoi = poi;
    },
    onUpdatePoiCoord (editingPoi) {
      const foundPoi = this.mapComp.newPois.find((poi) => {
        const coord = JSON.parse(poi.geom).coordinates[0];
        return editingPoi.oldCoord[0] === coord[0] && editingPoi.oldCoord[1] === coord[1];
      });
      if (foundPoi) {
        foundPoi.geom = JSON.stringify({
          type: 'MultiPoint',
          coordinates: [
            editingPoi.newCoord
          ],
          crs: {
            type: 'name',
            properties: {
              name: 'EPSG:3857'
            }
          }
        });
      }
    },
    onSaveButtonClick (force = true) {
      if (!this.mapComp.currentMode) {
        return;
      }
      switch (this.mapComp.currentMode) {
        case 'add':
          this.saveAddPois(force);
          break;
        case 'edit':
          this.saveEditPois();
          break;
        case 'remove':
          this.saveRemovePoi();
          break;
      }
    },
    async saveAddPois (force) {
      const newPois = this.mapComp.newPois;

      for (let i = 0; i < newPois.length; i++) {
        await this.addSinglePoi(newPois[i]);
      }

      this.updateTreeAfterAddPoi(force);
    },
    async saveAddPoi (poiData, imageFile, uploadFunction) {
      const { data } = await this.addSinglePoi(poiData);

      data && await uploadFunction(data.id, imageFile);
      this.updateTreeAfterAddPoi(true);
    },
    async addSinglePoi (poiData) {
      return await api.postRequest({
        endPoint: 'poi/',
        method: 'POST',
        data: poiData
      }, {
        baseApiUrl: process.env.BASE_API_URL,
        token: process.env.TOKEN
      });
    },
    updateTreeAfterAddPoi (force) {
      const treeComp = this.$refs.poiTree;
      treeComp.forceReloadNode = force;
      this.initialPoiCatId = [Number(this.mapComp.newPois[0].category)];
      if (force) {
        treeComp.loadDataToPoiTree();
      }
      this.$nextTick(() => {
        this.cleanUp(force, 'add');
      });
    },
    async saveEditPois () {
      if (!this.mapComp.editPois.length) {
        return;
      }

      for (let i = 0; i < this.mapComp.editPois.length; i++) {
        const poi = this.mapComp.editPois[i];
        const properties = { ...poi.getProperties() };

        await this.saveEditSinglePoi(poi, properties);
      }
      this.updateTreeAfterEditPoi(Number(this.mapComp.editPois[0].getProperties().category));
    },
    async saveEditPoi (poi, properties) {
      await this.saveEditSinglePoi(poi, properties);

      this.updateTreeAfterEditPoi(Number(poi.getProperties().category));
    },
    async saveEditSinglePoi (poi, properties) {
      const { floor_num: floorNum, short_name: floorName } = this.activeFloor;
      delete properties.geometry;

      if (!isNaN(floorNum) && floorName) {
        properties.floor_num = floorNum;
        properties.floor_name = floorName;
      }
      const data = {
        category: poi.getProperties().category,
        geometry: {
          type: 'MultiPoint',
          coordinates: poi.getGeometry().getCoordinates(),
          crs: {
            type: 'name',
            properties: {
              name: 'EPSG:3857'
            }
          }
        },
        properties
      };

      await api.putRequest({
        endPoint: `poi/${poi.getId()}/`,
        method: 'PUT',
        data
      }, {
        baseApiUrl: process.env.BASE_API_URL,
        token: process.env.TOKEN
      });
    },

    updateTreeAfterEditPoi (poiCatId) {
      const treeComp = this.$refs.poiTree;

      treeComp.forceReloadNode = true;
      this.initialPoiCatId = [poiCatId];

      if (!this.unsavedChanges) {
        treeComp.loadDataToPoiTree();
      }
      this.cleanupAndRemoveInteraction();
    },
    saveRemovePoi () {
      this.mapComp.deleteConfirm = true;
    },
    cleanUp (force = false, mode) {
      if (!force) {
        this.$root.$emit('addPoiClick');
      }
      this.cleanupAndRemoveInteraction();
    },
    async deletePois () {
      if (!this.mapComp.removePois.length) {
        return;
      }

      const removePois = this.mapComp.removePois;

      for (let i = 0; i < removePois.length; i++) {
        await this.deleteSinglePoi(removePois[i]);
      }

      this.updateTreeAfterEditPoi(Number(this.mapComp.removePois[0].getProperties().category));
    },

    async deletePoi (poi) {
      await this.deleteSinglePoi(poi);

      this.updateTreeAfterEditPoi(Number(poi.getProperties().category));
    },
    async deleteSinglePoi (poi) {
      await api.postRequest({
        endPoint: `poi/${poi.getId()}`,
        method: 'DELETE',
        data: {}
      }, {
        baseApiUrl: process.env.BASE_API_URL,
        token: process.env.TOKEN
      });
    },
    cleanupAndRemoveInteraction (clearAll = false) {
      this.unsavedChanges = false;
      this.mapComp.removeInteraction(true);
      this.mapComp.cleanUp();

      if (!clearAll) {
        this.$refs.map.onPoiLoad(this.lastLoadedData);
      }
    },
    handleAction (actionName) {
      if (this.changes) {
        this.unsavedChanges = true;
      } else {
        this.mapComp[actionName]();
      }
    }
  }
};
</script>

<style lang="scss" scoped>
  .save-btn-panel {
    position: absolute;
    top: 20px;
    position: absolute;
    left: calc(50% - 70px);
  }
  .poi {
    position: absolute;
    left: 10px;
    top: 20px;
    background: white;
    padding: 15px;
    border-radius: 5px;
  }
</style>
