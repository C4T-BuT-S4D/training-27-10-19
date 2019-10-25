import Vue from "vue";
import BootstrapVue from "bootstrap-vue";
import axios from "axios";
import lodash from "lodash";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

import App from "./App.vue";

axios.defaults.baseURL = "http://127.0.0.1:9999/api";

Vue.prototype.$http = axios;
Vue.prototype._ = lodash;
Vue.config.productionTip = false;
Vue.use(BootstrapVue);

new Vue({
  render: h => h(App)
}).$mount("#app");
