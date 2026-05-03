import { $fetch } from 'ofetch'
import config from './indrzConfig';
import LocalStorageService from '@/service/localStorage';

const { env } = config;

const getAuthorizationHeader = (tokenOverride) => {
  const header = {
    'Content-Type': 'application/json'
  };

  const userToken = LocalStorageService.getActiveToken();
  let token = tokenOverride || userToken || env.TOKEN;

  // Normalize tokens so env / overrides can be either raw (`abc`) or already prefixed (`Token abc`).
  if (typeof token === 'string') {
    token = token.trim();
    token = token.replace(/^token\s+/i, '');
    token = token.replace(/^bearer\s+/i, '');
  }

  if (token) {
    header.Authorization = `Token ${token}`;
  }
  return header;
};

const buildUrl = (endPoint = '', baseUrl) => {
  return `${baseUrl || env.BASE_API_URL || ''}${endPoint}`;
};

const request = async function (requestObj = {}, options = {}) {
  const url = buildUrl(requestObj.endPoint, options.baseApiUrl || requestObj.url);
  const headers = { ...getAuthorizationHeader(options.token), ...(requestObj.headers || {}) };

  const data = await $fetch(url, {
    method: requestObj.method || 'GET',
    headers,
    params: requestObj.params
  });

  return { data };
};

const postRequest = async function (requestObj = {}, options = {}) {
  let body = requestObj.data || {};
  const headers = { ...getAuthorizationHeader(options.token), ...(requestObj.headers || {}) };

  if (body instanceof FormData) {
    delete headers['Content-Type'];
  } else if (!(body instanceof Blob)) {
    const formData = new FormData();
    for (const [key, value] of Object.entries(body)) {
      formData.append(key, value === null ? '' : value);
    }
    body = formData;
    delete headers['Content-Type'];
  }

  const url = buildUrl(requestObj.endPoint, options.baseApiUrl || requestObj.url);

  const data = await $fetch(url, {
    method: requestObj.method || 'POST',
    headers,
    body
  });

  return { data };
};

const putRequest = async function (requestObj = {}, options = {}) {
  const url = buildUrl(requestObj.endPoint, options.baseApiUrl || requestObj.url);
  const headers = { ...getAuthorizationHeader(options.token), ...(requestObj.headers || {}) };

  const data = await $fetch(url, {
    method: requestObj.method || 'PUT',
    headers,
    body: requestObj.data
  });

  return { data };
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
