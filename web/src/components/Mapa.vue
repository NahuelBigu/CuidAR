<template>
  <div style="height: 93vh; ">
    <l-map style="height: 100%; width: 100%" :zoom="zoom" :minZoom="3" :center="center" :options="{worldCopyJump:true}">
      <l-tile-layer :url="url" :worldCopyJump="true"   :continuousWorld="false" :noWrap="true" ></l-tile-layer>

      <l-marker v-for="centro in centros " :key="centro.id"  :lat-lng="[centro.lat, centro.lng]">
      <!-- <l-icon         
          :icon-size="dynamicSize"
          :icon-anchor="dynamicAnchor"
          icon-url="https://cdn3.iconfinder.com/data/icons/gradient-general-pack/512/location-01-512.png"
        /> -->
        <l-popup >
          <div>
            <p class="mb-0 h5 "><strong>{{ centro.name }}</strong></p>{{ centro.opening_time.slice(0,-3) }} - {{ centro.closing_time.slice(0,-3) }}
            <div class="mt-2 mb-3">
             <strong> Direccion:</strong> {{ centro.address }} <br>
              <strong>  Web: </strong>
                <template  v-if="centro.web !=''"><a :href="'//' + centro.web" target="_blank">{{centro.web}} </a></template >
                <template  v-else>-</template > <br>
              <strong>  Telefono:</strong> {{ centro.phone }}
              
            </div>
            
          <button @click="innerClick(centro.id)" type="button" class="btn btn-sm btn-block btn-outline-primary" data-toggle="modal" data-target="#exampleModalCenter">
            Nuevo Turno
            </button>
           <!-- <button class="btn btn-sm btn-block btn-outline-primary" >
              Solicitar Turno
            </button> -->
          </div>
         
        </l-popup>
        
      </l-marker>
    </l-map>


    <!-- Modal -->
    <div class="modal fade" id="exampleModalCenter" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
        <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLongTitle">Solicitando turno</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
            </button>
        </div>
         
        <div class="modal-body">

             <div class="alert alert-danger mb-4 fade show" v-if="error">
               {{ error_message }}
               <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
              </div>
              
              <div class="alert alert-success mb-4" v-if="success_state">
               {{ success }}
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
              </div>

             
            <form  v-on:submit.prevent="mandar" id="turnForm" >
                <div class="form-group row">
                
                  <label class="col-sm-3 col-form-label">Fecha</label>
                
                <div class="col-sm-9">
                  <input type="date" name="date" id="date" class="form-control" v-model="turno.fecha" @change="modificar" required>
                </div>
              </div>
                <div class="form-group row">
                <div class="col-sm-6">
                  <label class="align-middle">Horario de inicio</label>
               
                  <select class="text-center form-control" v-model="turno.hora_inicio" @change="mod_closing_time" required style="text-align-last:center;">
                        <option class="text-center" v-for="option in hora_inicios" v-bind:key="option" v-bind:value="option">
                            {{ option.slice(0,-3) }}
                        </option>
                    </select>
                   
                </div>
                
                <div class="col-sm-6 ">
                   <label class="align-middle"> Hora de fin: </label>
                
               
               
                
                    <div class="align-middle"><span class="form-control" >{{turno.hora_fin}}</span></div>
                 </div>
                
                
              </div>
              
              <div class="form-group row">
                
                  <label class="col-sm-3 col-form-label">Nombre</label>
                
                <div class="col-sm-9">
                  <input type="text" name="nombre" class="form-control" id="nombre" v-model="turno.nombre" required>
                </div>
              </div>


              <div class="form-group row">
                
                  <label class="col-sm-3 col-form-label">Apellido</label>
                
                <div class="col-sm-9">
                  <input type="text" name="apellido" id="apellido" class="form-control" v-model="turno.apellido" required>
                </div>
              </div>
              <div class="form-group row ">
                
                  <label class="col-sm-3 col-form-label">Email</label>
                
                <div class="col-sm-9">
                 <input type="email" name="email_donante" id="email_donante" class="form-control" v-model="turno.email_donante" required>
                </div>
              </div>
              <div class="form-group row ">
                
                  <label class="col-sm-3 col-form-label">Telefono</label>
                
                <div class="col-sm-9">
                  <input type="tel" name="telefono_donante" id="telefono_donante" class="form-control" v-model="turno.telefono_donante" required>
                </div>
              </div>
                
            </form>
        </div>
        
        <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Cerrar</button>
            <input type="submit" form="turnForm" class="btn btn-primary" value="Solicitar turno">
        </div>
        
        </div>
    </div>
    </div>
  </div>
</template>
<script>
import {
  LMap,
  LTileLayer,
  LMarker,
  LPopup,
  
  LTooltip
} from "vue2-leaflet";
//import { latLng } from "leaflet";
import "leaflet/dist/leaflet.css";
import axios from "axios";
import Turno from "./Turno.vue";
export default {
  componets: {
    LMap,
    LTileLayer,
    LPopup,
    LMarker,
    LTooltip,
    Turno 
  },
  data() {
    return {
      url:
        "https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibmFodWVsYmlndSIsImEiOiJja2g2azdsYXUwM3FrMnNyN2wwdnl1YW8xIn0.Y6PFdcRQZkQRufGJLZh9IQ",
      zoom: 14,
      center: [-34.9187, -57.956],
      centros: [],
      showParagraph: true,
      iconSize: 45,

      turno: {
                centro_id: null,
                hora_inicio: "",
                hora_fin: "",
                email_donante:"",
                telefono_donante:"",
                fecha: "",
                nombre: "",
                apellido:""
            },
      error: false,
      success_state: false,
      success:"",
      error_message: '',
      hora_inicios: []
    };
  },
  computed: {
    dynamicSize() {
      return [this.iconSize, this.iconSize * 1.15];
    },
    dynamicAnchor() {
      return [this.iconSize / 2, this.iconSize * 1.15];
    },
  },
  mounted() {
    
    axios
      .get("https://admin-grupo72.proyecto2020.linti.unlp.edu.ar/centros?perPage=99999999")
      .then((response) => (this.centros = response.data.helpcenters.filter(x => x.lat != null)));
     
    
  },
  methods: {
    innerClick(id) {
      this.turno.centro_id=id
      this.success=""
      this.error_message=""
    },
     mandar() {    
          axios.post('https://admin-grupo72.proyecto2020.linti.unlp.edu.ar/centros/'+this.turno.centro_id+'/reserva',this.turno)
          .then(()=>{this.hora_inicios=[]
                    this.success="El turno se solicito correctamente"
                    this.success_state=true
                    this.error=false
                    this.error_message=""
                    this.turno.hora_inicio=""
                    this.turno.hora_fin=""
                    this.turno.email_donante=""
                    this.turno.nombre=""
                    this.turno.apellido=""
                    this.turno.telefono_donante=""
                    this.turno.fecha=""
                    this.turno.nombre=""
                    this.turno.apellido=""})
          .catch((error)=> {
            this.success_state=false
            this.error=true
            this.error_message=""
            for (let x in error.response.data.message){
                this.error_message=error.response.data.message[x][0] 
               break;
            }

            })
          
      
            
                      
        },
        modificar() {
            
            this.turno.hora_inicio=""
            this.turno.hora_fin=""
            axios
            .get('https://admin-grupo72.proyecto2020.linti.unlp.edu.ar/turnos/disponibles/'+this.turno.centro_id+'/'+(this.turno.fecha).replaceAll('-',''))
            .then(response => (this.hora_inicios = response.data))
            .catch(()=> {this.hora_inicios=[] })
        },
        mod_closing_time() {
            this.turno.hora_fin = new Date(new Date("1970/01/01 " + this.turno.hora_inicio).getTime() + 30 * 60000).toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit', hour12: false });
        }        
  },
};
</script>

<style>
  
</style>
