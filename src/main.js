import 'devextreme/dist/css/dx.common.css'
import 'devextreme/dist/css/dx.light.css'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store'
import VueProgressBar from 'vue-progressbar'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
require('../node_modules/bootstrap/dist/css/bootstrap.css')

Vue.config.productionTip = false

Vue.use(VueProgressBar, {
  color: 'rgb(143, 255, 199)',
  failedColor: 'red',
  height: '10px'
})
// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
