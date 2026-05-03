import View from 'ol/View';
import Map from 'ol/Map';
import Overlay from 'ol/Overlay';
import { defaults as defaultControls } from 'ol/control.js';
import { defaults as defaultInteraction } from 'ol/interaction';
import DragRotateAndZoom from 'ol/interaction/DragRotateAndZoom';
import PinchZoom from 'ol/interaction/PinchZoom';

import { getLayers, getMapControls } from '../map';
import { handleWindowResize } from './resize';

export const initializeMap = ({ mapId, predefinedPopup, center, zoom }) => {
  const view = new View({
    center,
    zoom,
    maxZoom: 23
  });

  const layers = getLayers();

  handleWindowResize(mapId);

  const map = new Map({
    interactions: defaultInteraction().extend([
      new DragRotateAndZoom(),
      new PinchZoom({
        constrainResolution: false
      })
    ]),
    target: mapId,
    controls: defaultControls({
      attribution: false,
      zoom: false
    }).extend(getMapControls()),
    view,
    layers: layers.layerGroups
  });

  const popup = predefinedPopup || new Overlay({
    element: document.getElementById('indrz-popup'),
    autoPan: true,
    autoPanAnimation: {
      duration: 250
    },
    zIndex: 5,
    name: 'indrzPopup'
  });

  map.addOverlay(popup);

  return {
    view, map, layers, popup
  };
};
