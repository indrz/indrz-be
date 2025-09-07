import Style from 'ol/style/Style';
import Stroke from 'ol/style/Stroke';
import Icon from 'ol/style/Icon';

const routeMarkerCStyle = new Style({
  image: new Icon({
    src: '/images/icons/routing/flag.png',
    anchor: [0.5, 1]
  }),
  zIndex: 6
});

const faCircleSolidStyle = new Style({
  image: new Icon({
    src: '/images/icons/routing/flag-blue.png',
    anchor: [0.5, 1],
    scale: 0.7
  }),
  zIndex: 6
});

const faFlagCheckeredStyle = new Style({
  image: new Icon({
    src: '/images/icons/routing/flag-checkered-blue.png',
    anchor: [0.5, 1],
    scale: 0.7
  }),
  zIndex: 6
});

const routeActiveStyleFront = new Style({
  stroke: new Stroke({
    color: '#158afc',
    width: 8
  }),
  zIndex: 6
});

const routeActiveStyleBackground = new Style({
  stroke: new Stroke({
    color: '#ffffff',
    width: 9,
    opacity: 0.5
  }),
  zIndex: 6
});

const routeActiveStyle = [routeActiveStyleBackground, routeActiveStyleFront];

const routeInactiveStyleBackground = new Style({
  stroke: new Stroke({
    color: '#ecf7ff',
    width: 8,
    opacity: 0.4
  }),
  zIndex: 6
});

const routeInactiveStyleForeground = new Style({
  stroke: new Stroke({
    color: '#1f9ffc',
    width: 4,
    lineDash: [1, 10],
    opacity: 0.1
  }),
  zIndex: 6
});

const routeInactiveStyle = [routeInactiveStyleBackground, routeInactiveStyleForeground];

const createPoiStyle = (poiIconName, active) => {
  const icon = `${poiIconName}`;
  const mainPoiIcons = ['education_active', 'access_active', 'security_active', 'infrastructure_active', 'services_active'];

  const iconDeactiveStyle = new Style({
    image: new Icon(/** @type {olx.style.IconOptions} */ ({
      anchor: [0.5, 46],
      anchorXUnits: 'fraction',
      anchorYUnits: 'pixels',
      opacity: 0.1,
      src: icon
    }))
  });

  const iconStyle = new Style({
    image: new Icon(/** @type {olx.style.IconOptions} */ ({
      anchor: [0.5, 46],
      anchorXUnits: 'fraction',
      anchorYUnits: 'pixels',
      src: icon
    }))
  });

  if (active === 'y') {
    return mainPoiIcons.includes(poiIconName) ? iconDeactiveStyle : iconStyle;
  } else {
    return iconDeactiveStyle;
  }
};

const setPoiStyleOnLayerSwitch = (iconName, visible) => {
  const icon = `${iconName}` || '';

  if (!icon) {
    return new Style({
      image: new Icon(/** @type {olx.style.IconOptions} */ ({
        anchor: [0.5, 46],
        anchorXUnits: 'fraction',
        anchorYUnits: 'pixels',
        opacity: 0,
        src: './noimage.png'
      }))
    });
  }

  const iconDeactiveStyle = new Style({
    image: new Icon(/** @type {olx.style.IconOptions} */ ({
      anchor: [0.5, 46],
      anchorXUnits: 'fraction',
      anchorYUnits: 'pixels',
      opacity: 0.1,
      src: icon
    }))
  });

  const iconActiveStyle = new Style({
    image: new Icon(/** @type {olx.style.IconOptions} */ ({
      anchor: [0.5, 46],
      anchorXUnits: 'fraction',
      anchorYUnits: 'pixels',
      opacity: 1,
      src: icon
    }))
  });

  if (visible) {
    return iconActiveStyle;
  } else {
    return iconDeactiveStyle;
  }
};

export default {
  routeActiveStyle,
  routeInactiveStyle,
  routeMarkerCStyle,
  faCircleSolidStyle,
  faFlagCheckeredStyle,
  setPoiStyleOnLayerSwitch,
  createPoiStyle
};
