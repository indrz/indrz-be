import config from '../util/indrzConfig';

export default ({ app }) => {
  config.set(app.$config);
}
