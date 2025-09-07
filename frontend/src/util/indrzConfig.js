const env = {};

const set = (processEnv) => {
  Object.assign(env, processEnv);
};

const get = () => {
  const maxTry = 100;
  let tryCount = 0;

  return new Promise((resolve) => {
    const interval = setInterval(() => {
      ++tryCount;

      if (env) {
        clearInterval(interval);
        resolve(env);
      }
    }, 50);
    if (tryCount === maxTry) {
      clearInterval(interval);
    }
  });
};

export default {
  env,
  set,
  get
}
