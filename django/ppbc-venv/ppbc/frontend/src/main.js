import Vue from 'vue';
import App from './App.vue';
import router from './router';
import VueResource from 'vue-resource';
/* Bootstrap */
import BootstrapVue from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
/* FontAwesome */
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
/* FontAwesome Icons */
import { faSyncAlt } from '@fortawesome/free-solid-svg-icons';
import {faCheck } from '@fortawesome/free-solid-svg-icons'
import { faArrowsAltV } from '@fortawesome/free-solid-svg-icons';
import { faFlask } from '@fortawesome/free-solid-svg-icons';
import { faSyringe } from '@fortawesome/free-solid-svg-icons';
import { faPrescriptionBottleAlt } from '@fortawesome/free-solid-svg-icons';

Vue.config.productionTip = false;

Vue.component('font-awesome-icon', FontAwesomeIcon);
library.add(faSyncAlt);
library.add(faArrowsAltV);
library.add(faPrescriptionBottleAlt);
library.add(faSyringe);
library.add(faFlask);
library.add(faCheck);

Vue.use(BootstrapVue);
Vue.use(VueResource);

new Vue({
  router,
  render: h => h(App),
}).$mount('#app');
