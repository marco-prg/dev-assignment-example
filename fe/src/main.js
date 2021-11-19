import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import i18n from './i18n'
import vuetify from './plugins/vuetify';
import axios from 'axios';
import '@/plugins/apexcharts';
import config from './config.json';   // required for dockerized version of the app (can't load .env file vars)

axios.defaults.baseURL = process.env.VUE_APP_BASE_URL ? process.env.VUE_APP_BASE_URL : config.VUE_APP_BASE_URL;
Vue.config.productionTip = false

new Vue({
  vuetify,
  router,
  store,
  i18n,
  render: h => h(App)
}).$mount('#app')
