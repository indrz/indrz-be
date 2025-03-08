import axios from 'axios';
import config from './indrzConfig';
import LocalStorageService from '@/service/localStorage';

const { env } = config;

const getAuthorizationHeader = () => {
  const header = {
    'Content-Type': 'application/json'
  };

  const userToken = LocalStorageService.getActiveToken();
  if (userToken) {
    header.Authorization = `Token ${userToken}`;
  } else if (env.TOKEN) {
    header.Authorization = env.TOKEN;
  }
  return header;
};

const request = function (requestObj) {
  return axios({
    url: `${requestObj.url || env.BASE_API_URL}${requestObj.endPoint || ''}`,
    method: requestObj.method || 'GET',
    headers: getAuthorizationHeader()
  });
};

const postRequest = async function (requestObj, options = {}) {
  try {
    let data;
    const headers = { ...getAuthorizationHeader(), ...(requestObj.headers || {}) };

    // If data is already FormData, use it directly
    if (requestObj.data instanceof FormData) {
      data = requestObj.data;
      // Don't set content-type for FormData; axios will add the boundary
      delete headers['Content-Type'];
    } else {
      // Otherwise create FormData from object
      const formData = new FormData();
      for (const [key, value] of Object.entries(requestObj.data || {})) {
        formData.append(key, value === null ? '' : value);
      }
      data = formData;
    }

    const axiosConfig = {
      url: `${options?.baseApiUrl || requestObj.url || env.BASE_API_URL}${requestObj.endPoint || ''}`,
      method: requestObj.method || 'POST',
      headers,
      data
    };

    // If transformRequest is provided, use it
    if (requestObj.transformRequest) {
      axiosConfig.transformRequest = requestObj.transformRequest;
    }

    return await axios(axiosConfig);
  } catch (err) {
    return err;
  }
};

const putRequest = async function (requestObj) {
  try {
    return await axios({
      url: `${requestObj.url || env.BASE_API_URL}${requestObj.endPoint || ''}`,
      method: requestObj.method || 'PUT',
      headers: getAuthorizationHeader(),
      data: requestObj.data
    })
  } catch (err) {
    return err;
  }
};

const getPageParams = ({ page = 1, itemsPerPage = 10 }) => {
  return {
    // page,
    limit: itemsPerPage,
    offset: (page - 1) * itemsPerPage
  }
};

const getURLParamsFromPayLoad = (payload) => {
  return payload ? `?${Object.keys(payload).map(key => key + '=' + payload[key]).join('&')}` : '';
};

export default {
  request,
  postRequest,
  putRequest,
  getPageParams,
  getURLParamsFromPayLoad
}
