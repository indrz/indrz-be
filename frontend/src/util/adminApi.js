import api from './api';

export const fetchFloors = async () => {
  try {
    const response = await api.request({
      endPoint: 'floor/'
    });
    return response.data.results;
  } catch (error) {
    console.error('Error fetching floors:', error);
    throw error; // Re-throw to handle it in the component
  }
};

export const fetchOrgcodeData = async (orgcode, floorNum) => {
  try {
    const response = await api.request({
      endPoint: `orgcode/${orgcode}/?floor_num=${floorNum}`
    });
    const geofc = response.data;
    if (geofc.features !== null) { return geofc } else {
      return null;
    }
  } catch (error) {
    console.error('Error fetching orgcode data:', error);
    throw error; // Re-throw to handle it in the component
  }
};
export const fetchOrganizationCodes = async () => {
  try {
    const response = await api.request({
      endPoint: 'orgcode'
    });
    const geofc = response.data;
    if (geofc.features !== null) { return geofc } else {
      return null;
    }
  } catch (error) {
    console.error('Error fetching orgcode data:', error);
    throw error; // Re-throw to handle it in the component
  }
}

export const fetchMainuseCategories = async () => {
  try {
    const response = await api.request({
      endPoint: 'mainuse'
    });
    const geofc = response.data;
    if (geofc.features !== null) { return geofc } else {
      return null;
    }
  } catch (error) {
    console.error('Error fetching mainUse data:', error);
    throw error; // Re-throw to handle it in the component
  }
}

export const fetchMainUseData = async (mainUse, floorNum) => {
  try {
    const response = await api.request({
      endPoint: `mainuse/${mainUse}/?floor_num=${floorNum}`
    });
    const geofc = response.data;
    if (geofc.features !== null) { return geofc } else {
      return null;
    }
  } catch (error) {
    console.error('Error fetching mainUse data:', error);
    throw error; // Re-throw to handle it in the component
  }
};
