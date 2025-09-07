import Api from '../util/api';

const signIn = (userInfo, env) => {
  return Api.postRequest({
    endPoint: 'api-token-auth/',
    data: userInfo
  }, env);
  /*
  return {
    data: {
      userName: userInfo.username,
      token: 'dummy-token'
    }
  };
  */
};

export default {
  signIn
};
