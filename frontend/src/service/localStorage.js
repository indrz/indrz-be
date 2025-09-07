const USER_TOKEN_KEY = 'indrz-user-token';

const setToken = (userData) => {
  sessionStorage.setItem(USER_TOKEN_KEY, JSON.stringify(userData));
};

const getTokenData = () => {
  const tokenData = sessionStorage.getItem(USER_TOKEN_KEY);
  return tokenData ? JSON.parse(tokenData) : null;
};

const getActiveToken = () => {
  const userData = getTokenData();
  return userData?.token || null;
};

const removeToken = () => {
  sessionStorage.removeItem(USER_TOKEN_KEY);
};

export default {
  setToken,
  getTokenData,
  getActiveToken,
  removeToken
};
