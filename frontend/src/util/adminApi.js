import axios from 'axios';
const API_BASE_URL = process.env.BASE_API_URL;
const AUTH_TOKEN = process.env.TOKEN

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    Authorization: AUTH_TOKEN
  }
});

export const fetchFloors = async () => {
  try {
    const response = await axiosInstance.get('floor/');
    return response.data.results;
  } catch (error) {
    console.error('Error fetching floors:', error);
    throw error; // Re-throw to handle it in the component
  }
};

export const fetchOrgcodeData = async (orgcode, floorNum) => {
  try {
    const response = await axiosInstance.get(`orgcode/${orgcode}/?floor_num=${floorNum}`);
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
    const response = await axiosInstance.get('/orgcode');
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
    const response = await axiosInstance.get('/mainuse');
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
    const response = await axiosInstance.get(`mainuse/${mainUse}/?floor_num=${floorNum}`);
    const geofc = response.data;
    if (geofc.features !== null) { return geofc } else {
      return null;
    }
  } catch (error) {
    console.error('Error fetching mainUse data:', error);
    throw error; // Re-throw to handle it in the component
  }
};
