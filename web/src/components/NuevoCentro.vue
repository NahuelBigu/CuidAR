
<template>

  <div>
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
    
      <div class="container mt-3">
       
        <div class="card">
          <div class="card-header">
            <h2>Solicitud de Nuevo Centro</h2>
          </div>
          <div class="card-body">
            <form @submit.prevent="onCreateCenter" id="formulario">

              <div class="form-group row">
                <label class='col-sm-2 col-form-label align-bottom'>Nombre del centro</label>
                
                <div class="col-sm-10">
                  <input type="text" name="name" class="form-control" v-model="centro.name" required>
                </div>
              </div>

              <div class="form-group row">
                <label class='col-sm-2 col-form-label align-bottom'>Direccion</label>
                
                <div class="col-sm-10">
                  <input type="text"  class="form-control" v-model="centro.address" required>
                </div>
              </div>

              <div class="form-group row">
                <label class='col-sm-2 col-form-label align-bottom'>Telefono</label>
                
                <div class="col-sm-10">
                  <input type="text" class="form-control" v-model="centro.phone" required>
                </div>
              </div>
              
              <div class="form-group row">
                <label class='col-sm-2 col-form-label align-bottom'>Horario de apertura</label>
                
                <div class="col-sm-10">
                  <input type="time" class="form-control mt-2" v-model="centro.opening_time" required>
                </div>
              </div>

              <div class="form-group row">
                <label class='col-sm-2 col-form-label align-bottom'>Horario de cierre</label>
                
                <div class="col-sm-10">
                  <input type="time" class="form-control mt-2" v-model="centro.closing_time" required>
                </div>
              </div>

              <div class="form-group row">
                <label class='col-sm-2 col-form-label align-bottom'>Tipo</label>
                
                <div class="col-sm-10">
                  <v-select multiple v-model="centro.type_center" :options="types" />
                </div>
              </div>

              <div class="form-group row">
                <label class='col-sm-2 col-form-label align-bottom'>Municipio</label>
                
                <div class="col-sm-10">
                  <select name="tipo" id="tipo" class="form-control" v-model="centro.municipio" required>
                    <option v-for="m in municipios" v-bind:key="m.id" :value="m.id">{{m.name}}</option>
                  </select>
                </div>
              </div>

              <div class="form-group row">
                <label class='col-sm-2 col-form-label align-bottom'>Web</label>
                
                <div class="col-sm-10">
                  <input type="url" class="form-control" v-model="centro.web">
                </div>
              </div>

              <div class="form-group row">
                <label class='col-sm-2 col-form-label align-bottom'>Email</label>
                
                <div class="col-sm-10">
                  <input type="email" class="form-control" v-model="centro.email">
                </div>
              </div>

              <div class="form-group row">
                <label class='col-sm-2 col-form-label align-bottom'>Ubicacion</label>
                
                <div class="col-sm-10">
                  <a id="abrirmapa" href="#addBookDialog" data-target="#addBookDialog" data-toggle="modal" data-username=""
                    title="Abrir Mapa" class="btn btn-light text-left btn-block open-AddBookDialog"  
                   @click="mapresize"  >Abrir Mapa</a>
                </div>
              </div>

              <div class="form-group row">
                <label class='col-sm-2 col-form-label align-bottom'>Protocolo de visita</label>
                
                <div class="col-sm-9 custom-file "  style="margin-left: 15px ;">
                  <input type="file" class="custom-file-input mt-2" id="file" ref="file" v-on:change="handleFileUpload()"/>
                   <label class="custom-file-label" for="inputGroupFile01">Elegir protocolo</label>
                </div>
              </div>

            </form>
            <div class="row justify-content-md-center mb-3">
                  
                 <div class="col-1">
                   <vue-recaptcha :sitekey="keycaptcha" @verify="recaptchaVerified" @expired="onCaptchaExpired" >
                     
                    </vue-recaptcha>
                </div>
                <div class="col-2 mr-5"></div>
            </div> 
            <div class="row justify-content-md-center">
              <div class="col col-4 ">
                   
                <button class="btn btn-success btn-block" type="submit" form="formulario"  v-if="captcha">Enviar</button>
                   
              </div>
            </div>   
               
          </div>
        </div>
    
    </div>
    
<!-- Modal -->
<div class="modal fade" id="addBookDialog" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle"
  aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLongTitle">Ubicacion </h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body" style="width: 100%;
    height: 400px;">
        
        <l-map style="height: 100%; width: 100%" :zoom="zoom" :center="center" ref="mymap" @click="addMarker">
          <l-tile-layer :url="url" ></l-tile-layer>
          <l-marker v-if="marker != null" :lat-lng="marker" @click="removeMarker"></l-marker>
        </l-map>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Cerrar</button>
        <button type="button" class="btn btn-danger" data-dismiss="modal" @click="removeMarker">Borrar
          Ubicacion</button>
        <button type="button" class="btn btn-success" data-dismiss="modal"  @click="confirmarUbicacion">Confirmar
          Ubicacion</button>
      </div>
    </div>
  </div>
</div>
  </div>
</template>

<script>

import axios from 'axios'
import "leaflet/dist/leaflet.css";
import VueRecaptcha from 'vue-recaptcha';
import vSelect from 'vue-select'
import 'vue-select/dist/vue-select.css';

export default {
  components:{
    VueRecaptcha,
    vSelect
  } ,
  data(){
    return {
      keycaptcha:"6LfqdP0ZAAAAAPOC0HPW0Lz5QeK102aS41Hx1C3U",
      types:[{label:'Comida',value:1},{label:'Ropa',value:2},{label:'Sangre',value:3}],
      municipios:[],
      cantM:[],
      centro:{
        name: '',
        address: '',
        phone: '',
        opening_time: '',
        closing_time: '',
        type_center: [],
        municipio: 0,
        web:'',
        email:'',
        latitud:"",
        longitud:"",
        view_protocol:''
      },
      url:
        "https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibmFodWVsYmlndSIsImEiOiJja2g2azdsYXUwM3FrMnNyN2wwdnl1YW8xIn0.Y6PFdcRQZkQRufGJLZh9IQ",
      zoom: 14,
      center: [-34.9187, -57.956],
      showParagraph: true,
      iconSize: 45,
      marker:null,
      captcha:false,
      error: false,
      success_state: false,
      success:"",
      error_message: '',
      file:null,
    }
  },
  methods: {
    onCreateCenter(){

      let formData = new FormData();
      formData.append('view_protocol', this.file);
      formData.append('name', this.centro.name);
      formData.append('address', this.centro.address);
      formData.append('phone', this.centro.phone);
      formData.append('opening_time', this.centro.opening_time);
      formData.append('closing_time', this.centro.closing_time);
      
      for(var x in this.centro.type_center){
        
          formData.append('type_center', this.centro.type_center[x].value);
      }
      
      formData.append('municipio', this.centro.municipio);
      formData.append('web', this.centro.web);
      formData.append('email', this.centro.email);
      formData.append('latitude', this.centro.latitud);
      formData.append('longitude', this.centro.longitud);
      
      if(this.captcha ){
           axios.post('https://admin-grupo72.proyecto2020.linti.unlp.edu.ar/centros', formData,{headers: {'Content-Type': 'multipart/form-data'}})
            .then(()=>{
              this.success="Se envio correctamente el nuevo centro para ser evaluado"
              this.success_state=true
              this.error=false
              this.error_message=""
              this.centro.name= '';
              this.centro.address= '';
              this.centro.phone= '';
              this.centro.opening_time= '';
              this.centro.closing_time= '';
              this.centro.type_center= [];
              this.centro.municipio= 0;
              this.centro.web='';
              this.centro.email='';
              this.centro.latitud=0;
              this.centro.longitud=0;
              this.centro.file=null
              this.centro.success="Felicidades"
              this.removeMarker()
            })
            .catch((Errors)=> {
            this.success_state=false
            this.error=true
            this.error_message=""
            for (let x in Errors.response.data.message){
                this.error_message+=Errors.response.data.message[x][0] 
                break;
            }

            })
            document.documentElement.scrollTop = 0;
      }
      
    },
    mapresize(){
      
      setTimeout(() => {
        //mapObject is a property that is part of leaflet
        this.$refs.mymap.mapObject.invalidateSize(); 
      }, 200);
    },
    addMarker(event) {
      this.marker=event.latlng;
      
    },
    removeMarker() {
      this.marker=null;
      this.centro.latitud=""
      this.centro.longitud=""
      if ( document.getElementById("abrirmapa").classList.contains('btn-primary') ){
          document.getElementById("abrirmapa").classList.remove('btn-primary');
          document.getElementById("abrirmapa").classList.add('btn-light');
      }
    },
    confirmarUbicacion(){
      this.centro.latitud=this.marker.lat
      this.centro.longitud=this.marker.lng
      document.getElementById("abrirmapa").classList.add('btn-primary');
      document.getElementById("abrirmapa").classList.remove('btn-light');
    },
    
    recaptchaVerified() {
      this.captcha=true
   
    },
    onCaptchaExpired(){
      this.captcha=false
    },
    handleFileUpload(){
        this.file = this.$refs.file.files[0];
      }

  },
  mounted:
    function (){
      axios.get('https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?per_page=150')
        .then(Response=>{this.municipios=Response.data.data.Town})
      
     
       let selectcss = document.createElement('link')
       
      selectcss.setAttribute('href', 'https://cdn.jsdelivr.net/npm/bootstrap-select@1.13.14/dist/css/bootstrap-select.min.css')
       selectcss.setAttribute('rel',"stylesheet")
      document.head.appendChild(selectcss)
      selectcss.async = true
       let selectjs = document.createElement('script')
      selectjs.setAttribute('src', 'https://cdn.jsdelivr.net/npm/bootstrap-select@1.13.14/dist/js/bootstrap-select.min.js')
      document.head.appendChild(selectjs)
      selectjs.async = true
    }
 
};
</script>



<style>
</style>