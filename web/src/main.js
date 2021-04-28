import Vue from 'vue'
import App from './App'

Vue.config.productionTip = false


import Test from "./components/Test.vue";
import Home from "./components/Home.vue";
import Mapa from "./components/Mapa.vue";
import Estadisticas from "./components/Estadisticas.vue";
import NuevoCentro from "./components/NuevoCentro.vue";
import Turno from "./components/Turno.vue"
import {LMap, LTileLayer,LMarker,LPopup,LIcon , LTooltip} from 'vue2-leaflet'
import VCharts from 'v-charts'
import VueRouter from 'vue-router';
import vSelect from 'vue-select'
import VeLine from 'v-charts/lib/line.common'
import VePie from 'v-charts/lib/pie.common'


Vue.component(VeLine.name, VeLine)
Vue.component("ve-pie", VePie)
Vue.use(VCharts)
Vue.component('v-select', vSelect)
Vue.use(VueRouter);
Vue.component('l-map', LMap);
Vue.component('l-tile-layer', LTileLayer);
Vue.component('l-marker', LMarker);
Vue.component('l-popup', LPopup);
Vue.component('l-icon',LIcon);
Vue.component('l-tooltip',LTooltip);
Vue.component('t-turno',Turno);
const router= new VueRouter({
  mode: 'history',
  base: __dirname,
  linkActiveClass: 'is-active',
  routes: [
    { path:'/',
      component: Home 
    },
    { path:'/mapa',
    component: Mapa 
    },
    { path:'/estadisticas',
    component: Estadisticas 
    },
    { path:'/nuevocentro',
    component: NuevoCentro 
    },
    { path: '/test',
      component: Test
    },
    { path: '/turno',
      component: Turno
    }
  ]

})
/* eslint-disable no-new */
new Vue({
  router,
  render: h => h(App),
  components: { App },
  template: '<App/>'
}).$mount('#app');

import { Icon } from 'leaflet';
delete Icon.Default.prototype._getIconUrl;
Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});